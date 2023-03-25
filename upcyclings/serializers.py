from rest_framework import serializers
from .models import UpcyclingCompany, UpcyclingPlastic


class UpcyclingPlasticSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UpcyclingPlastic
        fields = "__all__"


class UpcyclingCompanyListSerializer(serializers.ModelSerializer): # 전체 업사이클링 업체 조회
    
    class Meta:
        model = UpcyclingCompany
        fields = ('id', 'registrant', 'company', 'company_image', 'location')


class UpcyclingCompanySerializer(serializers.ModelSerializer): # 해당 업사이클링 업체 상세 페이지 (조회, 수정, 삭제)
    upcyclingplastic_company = UpcyclingPlasticSerializer(many=True)

    class Meta:
        model = UpcyclingCompany
        fields = ("company", "registrant", "company_image", "location", "contact_number", "upcyclingplastic_company")


class UpcyclingCompanyEnrollSerializer(serializers.ModelSerializer): # 업사이클링 업체 (등록)

    class Meta:
        model = UpcyclingCompany
        fields = ('company', 'company_image', 'location', 'contact_number')


class UpcyclingCompanyManagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpcyclingCompany
        fields = ('company', 'registrant')