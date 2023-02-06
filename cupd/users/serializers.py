import re
from rest_framework import serializers
from users.models import User
from django.core.exceptions import ValidationError


# 회원가입

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()
    nickname = serializers.CharField()

    class Meta:
        model = User
        fields = "__all__"

    def validate_email(self, data):
        email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_regex.match(data):
            raise ValidationError('INVALID_EMAIL_ADDRESS')
        elif User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email":"중복된 이메일이 있습니다."})
        return data

    def validate_password(self, data):
        password_regex = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
        if not password_regex.match(data):
            raise serializers.ValidationError('INVALID_PASSWORD')
        elif data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "패스워드가 일치하지 않습니다."})
        return data
        
    def validate_nickname(self, data):
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError({"nickname":"nickname을 두 글자 이상 작성해주세요."})
        if User.objects.filter(nickname=data["nickname"]).exists():
            raise serializers.ValidationError({"nickname":"중복된 닉네임이 있습니다."})
        return data

    def create(self, validated_data):
        user = super().create(validated_data) 
        password = user.password 
        user.set_password(password)
        user.save() 
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = user.password 
        user.set_password(password)
        user.save() 
        return user


#  마이페이지 프로필 정보 불러오기

class MypageInfoSerializer(serializers.ModelSerializer): # 수정 필요
    ecoprogram_likes = MypageWorkshopLikeSerializer(many=True)
    ecoprogram_host = WorkshopSerializer(many=True)
    ecoprogram_apply_guest = WorkshopApplySerializer(many=True)
    class Meta:
        model = User
        fields = ('nickname', 'email', 'profile_image', 'workshop_likes', 'hobby', 'workshop_host', 'workshop_apply_guest')


#  개인 프로필정보 수정

class MypageChangeInfoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password_check')

    def validate_email(self, data):
        email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_regex.match(data):
            raise ValidationError('INVALID_EMAIL_ADDRESS')
        elif User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email":"중복된 이메일이 있습니다."})
        return data

    def validate_nickname(self, data):
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError({"nickname":"nickname을 두 글자 이상 작성해주세요."})
        if User.objects.filter(nickname=data["nickname"]).exists():
            raise serializers.ValidationError({"nickname":"중복된 닉네임이 있습니다."})
        return data

    def validate_old_password(self, data): # 현재 비번 확인 
        user = self.context['request'].user # 로그인한 유저 정보 가져오기
        if not user.check_password(data): # 로그인한 유저의 비번이 아니라면
            raise serializers.ValidationError({"old_password": "기존 비밀번호가 아닙니다"})
        return data

    def validate_password(self, data):
        password_regex = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
        if not password_regex.match(data):
            raise serializers.ValidationError('INVALID_PASSWORD')
        elif data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "패스워드가 일치하지 않습니다."})
        return data

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.password = validated_data.get('password', instance.password)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

