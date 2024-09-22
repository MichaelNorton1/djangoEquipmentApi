from rest_framework import serializers
from .models import VibratoryHammer, Clamp, PowerPack, Bar, Jaw, RentalConfiguration, Customer, Component
from rest_framework import viewsets

class VibratoryHammerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VibratoryHammer
        fields = '__all__'


class ClampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clamp
        fields = '__all__'


class PowerPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerPack
        fields = '__all__'


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
        fields = '__all__'


class JawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jaw
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Component
        fields = '__all__'


class RentalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalConfiguration
        fields = '__all__'

  # def validate(self, data):
     ## needs check
   #     return





