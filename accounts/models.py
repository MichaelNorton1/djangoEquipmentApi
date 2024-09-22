from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


## These models are just base models and need to be updated

class Customer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class VibratoryHammer(models.Model):
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)  # Availability status

    def __str__(self):
        return self.serial_number


class Clamp(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)
    compatible_hammers = models.ManyToManyField(VibratoryHammer, related_name='compatible_clamps')
    is_available = models.BooleanField(default=True)


class PowerPack(models.Model):
    name = models.CharField(max_length=255)
    power_rating = models.DecimalField(max_digits=10, decimal_places=2)
    compatible_hammers = models.ManyToManyField(VibratoryHammer, related_name='compatible_power_packs')
    is_available = models.BooleanField(default=True)


class Bar(models.Model):
    name = models.CharField(max_length=255)
    compatible_hammers = models.ManyToManyField(VibratoryHammer, related_name='compatible_bars')
    is_available = models.BooleanField(default=True)


class Jaw(models.Model):
    name = models.CharField(max_length=255)
    compatible_hammers = models.ManyToManyField(VibratoryHammer, related_name='compatible_jaws')
    is_available = models.BooleanField(default=True)


class Component(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class RentalConfiguration(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hammer = models.ForeignKey(VibratoryHammer, on_delete=models.CASCADE, null=True, blank=True)
    clamp = models.ForeignKey(Clamp, on_delete=models.SET_NULL, null=True, blank=True)
    power_pack = models.ForeignKey(PowerPack, on_delete=models.SET_NULL, null=True, blank=True)
    bar = models.ForeignKey(Bar, on_delete=models.SET_NULL, null=True, blank=True)
    jaw = models.ForeignKey(Jaw, on_delete=models.SET_NULL, null=True, blank=True)
    rental_date = models.DateField()
    description = models.TextField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('reserved', 'Reserved'), ('rented', 'Rented'), ('out_of_service', 'Out of Service'),
                 ('completed', "Completed")],
        default='reserved'
    )

    def __str__(self):
        return f"Rental for {self.customer} - {self.hammer}"

    def clean(self):
        # Check if the hammer is available
        if not self.hammer.is_available:
            raise ValidationError(_('Selected hammer is not available.'))

        # Check if the clamp is available (if provided)
        if self.clamp and not self.clamp.is_available:
            raise ValidationError(_('Selected clamp is not available.'))

        # Check if the power pack is available (if provided)
        if self.power_pack and not self.power_pack.is_available:
            raise ValidationError(_('Selected power pack is not available.'))

        # Check if the bar is available (if provided)
        if self.bar and not self.bar.is_available:
            raise ValidationError(_('Selected bar is not available.'))

        # Check if the jaw is available (if provided)
        if self.jaw and not self.jaw.is_available:
            raise ValidationError(_('Selected jaw is not available.'))

    def save(self, *args, **kwargs):
        # Run the availability checks before saving
        self.clean()

        # Mark components as unavailable
        if self.hammer:
            self.hammer.is_available = False
            self.hammer.save()

        if self.clamp:
            self.clamp.is_available = False
            self.clamp.save()

        if self.power_pack:
            self.power_pack.is_available = False
            self.power_pack.save()

        if self.bar:
            self.bar.is_available = False
            self.bar.save()

        if self.jaw:
            self.jaw.is_available = False
            self.jaw.save()

        super().save(*args, **kwargs)
