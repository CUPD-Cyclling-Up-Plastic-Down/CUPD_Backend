from rest_framework import serializers
from users.models import User
from .models import Ecoprogram, EcoprogramApply, Review


class ReviewSerializer(serializers.ModelSerializer): # 특정 에코프로그램 상세조회에 사용되는 리뷰
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Review
        fields = ('id','user_id', 'content', 'user', 'profile_image', 'created_at', 'updated_at',)


class ReviewCreateSerializer(serializers.ModelSerializer): # 리뷰 작성(POST) 및 수정(PUT)

    class Meta:
        model = Review
        fields = ('content')


class EcoprogramApplySerializer(serializers.ModelSerializer): # 에코프로그램 신청
    guest_nickname = serializers.SerializerMethodField()
    ecoprogram = serializers.StringRelatedField()

    def get_guest_nickname(self, obj):
        return obj.guest.nickname

    class Meta:
        model = EcoprogramApply
        fields = ('id', 'ecoprogram_id', 'guest', 'guest_nickname', 'ecoprogram', 'result', 'created_at',)


class EcoprogramListSerializer(serializers.ModelSerializer): # 에코프로그램 전체 리스트 조회
    location = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_location(self, obj):
        return obj.location.district

    def get_date(self, obj):
        return obj.date.strftime('%Y년 %m월 %d일 %A')

    class Meta:
        model = Ecoprogram
        fields = ('title', 'content', 'host', 'location', 'ecoprogram_image', 'likes', 'views', 'organization', 'date')


class EcoprogramSerializer(serializers.ModelSerializer): # 특정 에코프로그램 상세 (조회, 등록, 수정)
    host = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    ecoprogram_apply = EcoprogramApplySerializer(many=True)
    review_ecoprogram = ReviewSerializer(many=True)
    review_ecoprogram_count = serializers.SerializerMethodField()

    def get_host(self, obj):
        return obj.host.nickname
    
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_location(self, obj):
        return obj.location.district

    def get_participant_count(self, obj):
        return obj.participant.count()

    def get_review_ecoprogram_count(self, obj):
        return obj.review_ecoprogram.count()

    class Meta:
        model = Ecoprogram
        fields = "__all__"