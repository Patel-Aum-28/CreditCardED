import os
import uuid
from django.shortcuts import render, redirect
from client.models import EncryptedData
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
import base64

def generate_unique_identifier():
    return str(uuid.uuid4())

def encrypt_data(data):
    try:
        identifier = generate_unique_identifier()

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        ciphertext = public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        key_folder = os.path.join("server", "private_keys", identifier)
        os.makedirs(key_folder, exist_ok=True)

        key_file_path = os.path.join(key_folder, f"{identifier}_private_key.pem")

        with open(key_file_path, 'wb') as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        return ciphertext, identifier

    except Exception as e:
        raise ValueError("Error encrypting data:", str(e))

def payment_form(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        card_holder = request.POST.get('card_holder')
        valid_thru = request.POST.get('valid_thru')
        cvv = request.POST.get('cvv')

        data_to_encrypt = f"{card_number} - {card_holder} - {valid_thru} - {cvv}"

        try:
            encrypted_data, identifier = encrypt_data(data_to_encrypt)
            encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')

            EncryptedData.objects.create(encrypted_data_base64=encrypted_data_base64, identifier=identifier)

            return render(request, 'client/index.html', {'message': 'Data successfully uploaded!'})

        except Exception as e:
            return render(request, 'client/index.html', {'error': e})

    return render(request, 'client/index.html')
