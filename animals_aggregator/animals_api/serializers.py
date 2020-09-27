from rest_framework import serializers
from animals_aggregator.models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ('__all__')
