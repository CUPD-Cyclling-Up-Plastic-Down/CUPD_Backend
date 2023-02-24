from django.contrib import admin
from .models import Location, Ecoprogram, EcoprogramApply, Review


class Lay_EcoprogramApply(admin.ModelAdmin):
    list_display = ['ecoprogram', 'guest', 'result', 'created_at']
admin.site.register(EcoprogramApply, Lay_EcoprogramApply)

class Lay_Review(admin.ModelAdmin):
    list_display = ['ecoprogram', 'user', 'content']
admin.site.register(Review, Lay_Review)

admin.site.register(Location)
admin.site.register(Ecoprogram)


