from unicodedata import name
from django.db import models
import string
import random


class User(models.Model):
    email = models.EmailField(unique=True)
    surname = models.CharField(max_length=100) # Nachname
    name = models.CharField(max_length=100)
    website = models.URLField()
    company = models.CharField(max_length=100)
    over_18 = models.BooleanField()
    password = models.CharField(max_length=256)
    private_pin = models.CharField(max_length=100) # Second password/pin for e.g. doors or jitsi

    class UserRole(models.TextChoices):
        CONTACT = 'CO', ('Contact')
        ATTENDANT = 'AT', ('Attendant')
        ORGANISATOR = 'OR', ('Organisatior')
        ADMIN = 'AD', ('Admin')

    user_role = models.CharField(
        max_length=2,
        choices=UserRole.choices,
        default=UserRole.CONTACT,
    )

    def __str__(self):
        return f"{self.email} - {self.surname} - {self.company}"

    def get_private_jitsi_url(self):
        return(f"https://jitsi.tux-tage.de/p_{self.surname}")
    
    def get_public_jitsi_url(self):
        return(f"https://jitsi.tux-tage.de/{self.surname}")

    def getUserRoleOfString(user_role_string):
        if user_role_string == 'CO':
            return User.UserRole.CONTACT
        elif user_role_string == 'AT':
            return User.UserRole.ATTENDANT
        elif user_role_string == 'OR':
            return User.UserRole.ORGANISATOR
        elif user_role_string == 'AD':
            return User.UserRole.ADMIN
        else:
            print(f"ERROR: getUserRoleOfString: no defined UserRole for {user_role_string}")
            return "Unknown!"

    def reset_password(self):
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        
        password = []
        for i in range(20):
            password.append(random.choice(characters))

        random.shuffle(password)
        self.password = "".join(password)
        self.save()
        print(f"new password = {self.password}")