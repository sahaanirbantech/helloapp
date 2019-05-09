from rest_framework import serializers
from .models import Hello


class HelloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hello
        fields = ('username', 'date_of_birth')
