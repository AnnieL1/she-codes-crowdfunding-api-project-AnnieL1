from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):  #Django has 'username' as a field inbuilt into AbstractUser. That's why a pass works in this case - there is already an inbuilt field 
    pass 

    def __str__ (self):
        return self.username #the string's method job is to turn something into text. In this case it will print the username in text so we know who is returning an error 