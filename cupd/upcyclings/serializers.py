from rest_framework import serializers
from users.models import User


class UpcyclingsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = 