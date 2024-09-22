from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import VibratoryHammer, Clamp, PowerPack, Bar, Jaw, Customer, RentalConfiguration

admin.site.register(VibratoryHammer)
admin.site.register(Clamp)
admin.site.register(PowerPack)
admin.site.register(Bar)
admin.site.register(Jaw)
admin.site.register(Customer)
admin.site.register(RentalConfiguration)
