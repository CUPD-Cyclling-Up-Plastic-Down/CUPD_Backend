import re
from rest_framework import serializers
from users.models import Consumer, Organization
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ecoprograms.serializers import EcoprogramApplySerializer, EcoprogramApplyResultSerializer
from ecoprograms.models import Ecoprogram, EcoprogramApply
from upcyclings.models import UpcyclingCompany
from upcyclings.serializers import UpcyclingCompanyManagementSerializer


# 회원가입(소비자)

class SignUpConsumerSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
    nickname = serializers.CharField()

    class Meta:
        model = Consumer
        fields = ("type", "nickname", "email", "password")

    def validate(self, data):
        
        email = data["email"]
        email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"])
        if not email_validation.fullmatch(email) :
            raise serializers.ValidationError({"email":"이메일 형식을 확인해주세요"})

        if Consumer.objects.filter(nickname=data["nickname"]).exists():
                raise serializers.ValidationError({"nickname":"중복된 닉네임이 있습니다."})
        
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError({"nickname":"nickname을 두 글자 이상 작성해주세요."})

        elif len(data["password"]) < 2 or password:
            raise serializers.ValidationError({"password":"password는  2자 이상 특수문자 포함 "})
        
        return data

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.password = validated_data.get('password', instance.password)
        instance.set_password(validated_data[1])
        instance.save()
        return instance


# 회원가입(환경단체)

class SignUpOrganizationSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
    nickname = serializers.CharField()

    class Meta:
        model = Organization
        fields = ("type", "nickname", "email", "password")

    def validate(self, data):
        
        email = data["email"]
        email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"])
        if not email_validation.fullmatch(email) :
            raise serializers.ValidationError({"email":"이메일 형식을 확인해주세요"})

        if Organization.objects.filter(nickname=data["nickname"]).exists():
                raise serializers.ValidationError({"nickname":"중복된 닉네임이 있습니다."})
        
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError({"nickname":"nickname을 두 글자 이상 작성해주세요."})

        elif len(data["password"]) < 2 or password:
            raise serializers.ValidationError({"password":"password는  2자 이상 특수문자 포함 "})

        return data

    def create(self, validated_data):
        user = super().create(validated_data) 
        password = user.password
        user.set_password(password)
        user.save() 
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.password = validated_data.get('password', instance.password)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance



# jwt 토큰 발급

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['nickname'] = user.nickname  
        # ...
        return token


# 마이페이지(소비자)

class MypageEcoprogramLikeSerializer(serializers.ModelSerializer):  # (소비자): 좋아요한 에코프로그램
    location = serializers.SerializerMethodField()
    
    def get_location(self, obj):
        return obj.location.district
    
    class Meta:
        model = Ecoprogram
        fields = ( 'id', 'host', 'title', 'ecoprogram_image', 'location', 'address2', 'likes')


class MypageEcoprogramAppliedSerializer(serializers.ModelSerializer): # (소비자): 신청한 에코프로그램
    ecoprogram = serializers.SerializerMethodField()

    def get_ecoprogram(self, obj):
        return obj.ecoprogram.title

    class Meta:
        model = EcoprogramApply
        fields = ('ecoprogram', 'result', 'created_at')


class MypageEcoprogramConfirmedSerializer(serializers.ModelSerializer): # (소비자): 참여확정된 에코프로그램
    ecoprogram = serializers.SerializerMethodField()

    def get_ecoprogram(self, obj):
        return obj.ecoprogram.title
    
    class Meta:
        model = EcoprogramApply
        fields = ('ecoprogram', 'result', 'created_at')


class MypageConsumerInfoSerializer(serializers.ModelSerializer): # (소비자): 프로필 정보 불러오기
    ecoprogram_likes = MypageEcoprogramLikeSerializer(many=True)
    ecoprogram_apply_guest = EcoprogramApplySerializer(many=True)

    class Meta:
        model = Consumer
        fields = ('nickname', 'email', 'profile_image', 'ecoprogram_likes', 'ecoprogram_apply_guest')


class MypageConsumerProfileEditSerializer(serializers.ModelSerializer): # (소비자): 마이페이지 프로필 정보 수정
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Consumer
        fields = ('email', 'nickname', 'old_password', 'password',)

    def validate(self, data):
        
        email = data["email"]
        email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"])
        if not email_validation.fullmatch(email) :
            raise serializers.ValidationError({"email":"이메일 형식을 확인해주세요"})

        if Consumer.objects.filter(nickname=data["nickname"]).exists():
            raise serializers.ValidationError({"nickname":"중복된 닉네임이 있습니다."})
        
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError({"nickname":"nickname을 두 글자 이상 작성해주세요."})

        elif len(data["password"]) < 2 or password:
            raise serializers.ValidationError({"password":"password는  2자 이상 특수문자 포함 "})

        return data
    
    def validate_old_password(self, data): # 현재 비번 확인 
        user = self.context['request'].user # 로그인한 유저 정보 가져오기
        if not user.check_password(data): # 로그인한 유저의 비번이 아니라면
            raise serializers.ValidationError({"old_password": "기존 비밀번호가 아닙니다"})
        return data

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.password = validated_data.get('password', instance.password)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


# 마이페이지(환경단체)

class MypageEcoprogramCreatedSerializer(serializers.ModelSerializer): # (환경단체): 생성한 에코프로그램 조회 및 삭제
    
    class Meta:
        model = Ecoprogram
        fields = ('title', 'due_date', 'host', 'created_at', 'updated_at', 'participant', 'max_guest')


class MypageEcoprogramApplyResultSerializer(serializers.ModelSerializer): # (환경단체): 해당 에코프로그램 신청 인원 결과 (조회)

    class Meta:
        model = EcoprogramApply
        fields = ('ecoprogram', 'guest', 'result')


class MypageUpcyclingCompanyManagementSerializer(serializers.ModelSerializer): # (환경단체): 업체 등록 관리

    class Meta:
        model = UpcyclingCompany
        fields = ('company',)


class MypageOrganizationInfoSerializer(serializers.ModelSerializer): # (환경단체): 프로필 정보(조회)

    class Meta:
        model = Organization
        fields = ('nickname', 'email', 'profile_image',)


class MypageOrganizationProfileEditSerializer(serializers.ModelSerializer): # (환경단체): 프로필 정보(수정)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Organization
        fields = ('email', 'nickname', 'old_password', 'password')

    def validate(self, data):
        
        email = data["email"]
        email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"])
        if not email_validation.fullmatch(email) :
            raise serializers.ValidationError({"email":"이메일 형식을 확인해주세요"})

        if Organization.objects.filter(nickname=data["nickname"]).exists():
                raise serializers.ValidationError({"nickname":"중복된 닉네임이 있습니다."})
        
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError({"nickname":"nickname을 두 글자 이상 작성해주세요."})

        elif len(data["password"]) < 2 or password:
            raise serializers.ValidationError({"password":"password는  2자 이상 특수문자 포함 "})

        return data

    def validate_old_password(self, data): # 현재 비번 확인 
        user = self.context['request'].user # 로그인한 유저 정보 가져오기
        if not user.check_password(data): # 로그인한 유저의 비번이 아니라면
            raise serializers.ValidationError({"old_password": "기존 비밀번호가 아닙니다"})
        return data

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.password = validated_data.get('password', instance.password)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance