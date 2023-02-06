from django.db import models
from users.models import User
from .utils import rename_imagefile_to_uuid
from django.core.validators import RegexValidator


class Location(models.Model):
    district = models.CharField(max_length=10)

    def __str__(self):
        return str(self.district)


class ContactNumber(models.Model):
    contact_number_regex = RegexValidator(regex = r'^0([2|31|32|33|41|42|43|44|51|52|53|54|55|61|62|63|64]?)-?([0-9]{3,4})-?([0-9]{4})')
    contact_number = models.CharField(validators=[contact_number_regex], max_length=11, unique=True)


class UpcyclingCompany(models.Model):
    company_name = models.CharField(max_length=20)
    registrant = models.OneToOneField(User, on_delete=models.CASCADE)
    company_image = models.ImageField(upload_to=rename_imagefile_to_uuid)
    contact_number = models.ForeignKey(ContactNumber, on_delete=models.CASCADE, related_name='upcycling_contact_number')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='upcycling_location')

    def __str__(self):
        return str(self.company_name)
    
    
class UpcyclingPlastic(models.Model):
    plastic_name = models.CharField(max_length=20)
    classification = models.CharField(max_length=20)
    weight = models.PositiveIntegerField()

    def __str__(self):
        return str(self.plastic_name)

