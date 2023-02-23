from django.db import models
from users.models import Organization
from .utils import rename_imagefile_to_uuid
from django.core.validators import RegexValidator


class Location(models.Model):
    district = models.CharField(max_length=10)

    def __str__(self):
        return str(self.district)


class UpcyclingCompany(models.Model):
    company = models.CharField(max_length=20)
    registrant = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='upcyclingcompany_registrant')
    company_image = models.ImageField(upload_to=rename_imagefile_to_uuid)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    contact_number_regex = RegexValidator(regex = r'^0([2|31|32|33|41|42|43|44|51|52|53|54|55|61|62|63|64]?)-?([0-9]{3,4})-?([0-9]{4})')
    contact_number = models.CharField(validators=[contact_number_regex], max_length=11, unique=True)

    def __str__(self):
        return str(self.company)
    
    
class UpcyclingPlastic(models.Model):
    plastic = models.CharField(max_length=30)
    classification = models.CharField(max_length=20)
    weight = models.PositiveIntegerField(default=0)
    amount_per_weight = models.PositiveIntegerField(default=0)
    expected_refund = models.PositiveIntegerField(default=0, null=True)
   
    def __str__(self):
        return str(self.plastic)

    def save(self):
        self.expected_refund = (self.weight)*(self.amount_per_weight) # 예상 환급 금액
        super().save()




