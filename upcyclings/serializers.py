from rest_framework import serializers
from users.models import User
from .models import UpcyclingCompany, UpcyclingPlastic


class UpcyclingPlasticSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UpcyclingPlastic
        fields = "__all__"

    # def __mul__(self):
    #     expected_refund = (UpcyclingPlastic.weight)*(UpcyclingPlastic.amount_per_weight) # 예상 환급 금액
    #     return expected_refund
    
    # expected_refund = __mul__()


class UpcyclingCompanyListSerializer(serializers.ModelSerializer): # 전체 업사이클링 업체 조회
    
    class Meta:
        model = UpcyclingCompany
        fields = ('registrant', 'company', 'company_image', 'location')


class UpcyclingCompanySerializer(serializers.ModelSerializer): # 해당 업사이클링 업체 상세 페이지 (조회, 수정, 삭제)
    plastic = UpcyclingPlasticSerializer(many=True)

    class Meta:
        model = UpcyclingCompany
        fields = "__all__"


class UpcyclingCompanyEnrollSerializer(serializers.ModelSerializer): # 업사이클링 업체 (등록)
    plastic = UpcyclingPlasticSerializer(many=True)

    class Meta:
        model = UpcyclingCompany
        fields = "__all__"


class UpcyclingCompanyManagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpcyclingCompany
        fields = ('company', 'registrant')