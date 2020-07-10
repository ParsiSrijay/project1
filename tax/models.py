from django.db import models

# Create your models here.
class imo(models.Model):
    Name=models.CharField(max_length=20)
    Address=models.CharField(max_length=50)
    State=models.CharField(max_length=20)
    Phone_Number=models.IntegerField()
    Registration_id_imo=models.IntegerField()
    Password=models.CharField(max_length=20)
    Head_of_IMO=models.CharField(max_length=20)