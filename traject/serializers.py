from rest_framework import serializers
from .models import Trajet, JournalELD

class TrajetSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  # Gérer ObjectId comme une chaîne

    class Meta:
        model = Trajet
        fields = '__all__'

class JournalELDSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  # Gérer ObjectId comme une chaîne

    class Meta:
        model = JournalELD
        fields = '__all__'