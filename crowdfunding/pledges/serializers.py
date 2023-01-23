from rest_framework import serializers

class PledgesSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.FloatField()
