import os
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from client.models import EncryptedData
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.hazmat.backends import default_backend
import base64

def decrypt_data(encrypted_data_base64, private_key_pem):
    encrypted_data = base64.b64decode(encrypted_data_base64)

    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend()
    )
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data.decode()

def encrypted_data_list(request):
    encrypted_data_list = EncryptedData.objects.all()
    return render(request, 'server/encrypted_data_list.html', {'encrypted_data_list': encrypted_data_list})

def decrypt_data_view(request, encrypted_data_id):
    try:
        encrypted_data = EncryptedData.objects.get(identifier=encrypted_data_id)
    except ObjectDoesNotExist:
        return redirect('server:encrypted_data_list') 

    if request.method == 'POST':
        selected_key = request.FILES.get('selected_key')
        if selected_key:
            try:
                private_key_pem = selected_key.read()
                decrypted_data = decrypt_data(encrypted_data.encrypted_data_base64, private_key_pem)
                decrypted_data_list = decrypted_data.split(" - ")
                return render(request, 'server/decrypt_data.html', {'encrypted_data': encrypted_data, 'decrypted_data_list': decrypted_data_list})
            except Exception as e:
                error_message = f"Error decrypting data: {e}"
                return render(request, 'server/decrypt_data.html', {'encrypted_data': encrypted_data, 'error_message': error_message})

    return render(request, 'server/decrypt_data.html', {'encrypted_data': encrypted_data})
