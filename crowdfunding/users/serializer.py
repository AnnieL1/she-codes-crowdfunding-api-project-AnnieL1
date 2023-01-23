from rest_framework import serializers 
from .models import CustomUser

class CustomUserSerializer(serializers.Serializer):  # don't put pw here cos you never want pw to be pulled out of database
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField()

    def create(self, validated_data):   #this part will either accept or reject the pw. PW is sent to db as hashes and if the hashes sent matches the hatches in db then pw is correct. Hashes are used since it's hard to read and translate to normal letters do it's hard to hack.
        return CustomUser.objects.create(**validated_data)