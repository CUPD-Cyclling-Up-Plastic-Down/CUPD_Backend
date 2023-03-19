from django.db import models
from users.models import User
from .utils import rename_imagefile_to_uuid


class Location(models.Model):
    district = models.CharField(max_length=20)

    def __str__(self):
        return str(self.district)


class Ecoprogram(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=20)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ecoprogram_host')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='ecoprogram_location')
    ecoprogram_image = models.ImageField(upload_to=rename_imagefile_to_uuid)
    introduce = models.TextField(max_length=50)
    likes = models.ManyToManyField(User, related_name='ecoprogram_likes', blank=True)
    views = models.BigIntegerField(default=0)
    organization = models.CharField(max_length=20)
    due_date = models.DateTimeField()
    cost = models.PositiveIntegerField()
    participant = models.ManyToManyField(User, related_name='ecoprogram_participant', blank=True, through='EcoprogramApply', through_fields=('ecoprogram', 'guest'),)
    max_guest = models.IntegerField()
    address2 = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
    
class EcoprogramApply(models.Model):
    CHOICES_APPLY = [
        ('APPROVE', '승인'),
        ('REJECTION', '거절'),
        ('WAITING', '대기'),
    ]
    ecoprogram = models.ForeignKey(Ecoprogram, on_delete=models.CASCADE, related_name='ecoprogram_apply')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ecoprogram_apply_guest')
    result = models.CharField('신청유형', choices=CHOICES_APPLY, default='WAITING', null=True, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ecoprogram_apply"

    def __str__(self):
        return str(self.ecoprogram)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    ecoprogram = models.ForeignKey(Ecoprogram, on_delete=models.CASCADE, related_name='review_ecoprogram')
    content = models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)