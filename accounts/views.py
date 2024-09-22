from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import login, logout
from rest_framework import viewsets

from .models import VibratoryHammer, Clamp, PowerPack, Bar, Jaw, Customer
from .serializers import VibratoryHammerSerializer, ClampSerializer, PowerPackSerializer, BarSerializer, JawSerializer, \
    CustomerSerializer, RentalsSerializer, ComponentsSerializer
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VibratoryHammer, Clamp, PowerPack, Bar, Jaw, Component, RentalConfiguration


class CreateRentalConfigurationView(APIView):

    def post(self, request):
        print(request)

        if request.user.is_authenticated:
            print(f"Authenticated user: {request.user.username}")
        else:
            print("User is not authenticated.")
            #### this is wrong
        hammer_id = request.data.get('hammer_id')
        clamp_id = request.data.get('clamp_id')
        power_pack_id = request.data.get('power_pack_id')
        bar_id = request.data.get('bar_id')
        jaw_id = request.data.get('jaw_id')
        additional_components = request.data.get('additional_components', [])
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        hammer = VibratoryHammer.objects.get(id=hammer_id)
        clamp = Clamp.objects.get(id=clamp_id)
        power_pack = PowerPack.objects.get(id=power_pack_id)
        bar = Bar.objects.get(id=bar_id)
        jaw = Jaw.objects.get(id=jaw_id)

        # Check availability
        if not RentalConfiguration.is_available(hammer, clamp, power_pack, bar, jaw, start_date, end_date):
            return Response({"error": "Equipment is not available for the selected period."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create RentalConfiguration
        rental_config = RentalConfiguration.objects.create(
            hammer=hammer,
            clamp=clamp,
            power_pack=power_pack,
            bar=bar,
            jaw=jaw,
            start_date=start_date,
            end_date=end_date
        )
        rental_config.additional_components.set(additional_components)
        rental_config.save()

        return Response({"message": "Rental configuration created successfully"}, status=status.HTTP_201_CREATED)





@api_view(['GET'])
def check_authentication(request):
    if request.user.is_authenticated:
        return Response({"isAuthenticated": True})
    return Response({"isAuthenticated": False})


class VibratoryHammerViewSet(viewsets.ModelViewSet):
    queryset = VibratoryHammer.objects.all()
    serializer_class = VibratoryHammerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ClampViewSet(viewsets.ModelViewSet):
    queryset = Clamp.objects.all()
    serializer_class = ClampSerializer


class PowerPackViewSet(viewsets.ModelViewSet):
    queryset = PowerPack.objects.all()
    serializer_class = PowerPackSerializer


class BarViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer


class JawViewSet(viewsets.ModelViewSet):
    queryset = Jaw.objects.all()
    serializer_class = JawSerializer


class RentalsViewSet(viewsets.ModelViewSet):
    queryset = RentalConfiguration.objects.all()
    serializer_class = RentalsSerializer


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentsSerializer


class CustomerRentalViewSet(viewsets.ModelViewSet):
    serializer_class = RentalsSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        if customer_id is None:
            return RentalConfiguration.objects.none()  # or raise an exception

            # Return rentals filtered by customer_id
        return RentalConfiguration.objects.filter(customer_id=customer_id)


class CustomLoginView(LoginView):
    # Specify the template for the login form (if needed)
    template_name = 'accounts/login.html'

    # Override the form_valid method to generate the token and redirect
    def form_valid(self, form):
        # Log the user in
        response = super().form_valid(form)

        # Generate a JWT token
        user = self.request.user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Redirect to Vue.js app with the token in the URL

        response = HttpResponseRedirect('http://localhost:5173/')
        response.set_cookie('access_token', access_token, httponly=True, samesite='Lax', max_age=3600)

        return response


def logout_view(request):
    logout(request)
    return redirect('login')
