from django.db import models

class EncryptedData(models.Model):
    encrypted_data_base64 = models.TextField()
    identifier = models.CharField(max_length=36)
