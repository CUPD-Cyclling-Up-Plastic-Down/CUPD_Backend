from django.contrib import admin
from .models import Location, Ecoprogram, EcoprogramApply, Review


admin.site.register(Location)
admin.site.register(Ecoprogram)
admin.site.register(EcoprogramApply)
admin.site.register(Review)
