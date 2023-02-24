from django.contrib import admin
from .models import Location, Ecoprogram, EcoprogramApply, Review


admin.site.register(Location)
admin.site.register(Ecoprogram)
admin.site.register(Review)


class Lay_EcoprogramApply(admin.ModelAdmin):
    list_display = ['ecoprogram', 'guest', 'result', 'created_at']

admin.site.register(EcoprogramApply, Lay_EcoprogramApply)