from rest_framework import serializers
from .models import Project, Pledge

class PledgeSerializer(serializers.ModelSerializer):  #modelSerializer is programmed to look at the fields in the model and match up what it has been asked to serialise from models.py   
#if change to 'Meta' you also have to change, you also have to change views.py
    class Meta:
        model = Pledge
        fields = ['id', 'amount', 'comment', 'anonymous', 'project', 'supporter']
        read_only_fields = ['id', 'supporter']
    # id = serializers.ReadOnlyField()
    # amount = serializers.IntegerField()
    # comment = serializers.CharField(max_length=200)
    # anonymous = serializers.BooleanField() #anon is in backend because when BE receives a list of pledges it's just going to contain a list of data from the database. Need to tell it to be anon so it doesn't display everyone's data or data a pledger doesn't want FE to show 
    # supporter = serializers.CharField(max_length=200)
    # project_id = serializers.IntegerField()

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)

class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.id')

    def create(self, validated_data):
        return Project.objects.create(**validated_data) # ** is an unpacking syntax ie. if you recieve a dictionary, unpack the dictionary and hand each key value pair over as a key arguement

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    
    def update(self, instance, validated_data): 
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance 

    
