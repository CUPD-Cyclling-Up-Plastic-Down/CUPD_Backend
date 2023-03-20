from rest_framework import serializers
from .models import Ecoprogram, EcoprogramApply, Review


# 특정 에코프로그램 상세조회에 사용되는 리뷰

class EcoprogramReviewSerializer(serializers.ModelSerializer): 
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Review
        fields = ('id','user_id', 'user', 'content', 'created_at', 'updated_at',)


 # 리뷰 작성(POST)

class EcoprogramReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('content',)


 # 리뷰 수정(PUT)

class EcoprogramReviewEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('content',)


 # 에코프로그램 신청

class EcoprogramApplySerializer(serializers.ModelSerializer):
    guest_nickname = serializers.SerializerMethodField()
    ecoprogram = serializers.StringRelatedField()

    def get_guest_nickname(self, obj):
        return obj.guest.nickname

    class Meta:
        model = EcoprogramApply
        fields = ('id', 'ecoprogram_id', 'guest', 'guest_nickname', 'ecoprogram', 'result', 'created_at',)


 # 에코프로그램 전체 리스트 조회

class EcoprogramListSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_location(self, obj):
        return obj.location.district

    def get_date(self, obj):
        return obj.date.strftime('%Y년 %m월 %d일 %A')

    class Meta:
        model = Ecoprogram
        fields = ('title', 'content', 'host', 'location', 'ecoprogram_image', 'likes', 'views', 'organization', 'due_date',)


 # 특정 에코프로그램 상세 (조회)

class EcoprogramSerializer(serializers.ModelSerializer):
    host = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    ecoprogram_apply = EcoprogramApplySerializer(many=True)
    review_ecoprogram = EcoprogramReviewSerializer(many=True)
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


# 에코프로그램 등록

class EcoprogramEnrollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ecoprogram
        fields = ("host", "ecoprogram_image", "title", "introduce", "cost", "due_date", "max_guest", "location", "address2", "organization")


# 에코프로그램 수정

class EcoprogramEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ecoprogram
        fields = ("host", "ecoprogram_image", "title", "introduce", "cost", "due_date", "max_guest", "location", "address2", "organization")


