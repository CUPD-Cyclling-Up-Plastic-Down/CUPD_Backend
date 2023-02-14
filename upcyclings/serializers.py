from rest_framework import serializers
from users.models import User
from .models import UpcyclingCompany, UpcyclingPlastic


class UpcyclingPlasticSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpcyclingPlastic
        fields = "__all__"


class UpcyclingCompanyListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UpcyclingCompany
        fields = ('registrant', 'company', 'company_image', 'location')


class UpcyclingCompanySerializer(serializers.ModelSerializer):
    plastic = UpcyclingPlasticSerializer(many=True)

    class Meta:
        model = UpcyclingCompany
        fields = "__all__"


class UpcyclingCompanyManagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpcyclingCompany
        fields = ('company', 'registrant')