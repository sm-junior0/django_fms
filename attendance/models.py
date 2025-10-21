from django.db import models
from django.utils import timezone 

# Create your models here.

class Farmer(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    EMPLOYMENT_CHOICES = [
        ('casual', 'Casual'),
        ('contract', 'Contract'),
    ]
    
    name=models.CharField(max_length=100)
    farm=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    gender=models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    employment_type=models.CharField(max_length=10, choices=EMPLOYMENT_CHOICES, default='casual')

    class Meta :                    
        db_table='farmer'

    def  __str__(self):
        return self.name+" - "+self.farm

class Attendance(models.Model):
    date=models.DateField(default=timezone.now)
    is_present=models.BooleanField(default=False)
    farmer=models.ForeignKey(Farmer,on_delete=models.CASCADE)   
    
    class Meta : 
        db_table='attendance'

    def  __str__(self):
        return self.farmer.name