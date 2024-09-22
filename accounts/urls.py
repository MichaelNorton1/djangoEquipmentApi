from django.urls import path
from .views import logout_view, CustomLoginView, CustomerViewSet, RentalsViewSet, ComponentViewSet, \
    CreateRentalConfigurationView, CustomerRentalViewSet, check_authentication

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VibratoryHammerViewSet, ClampViewSet, PowerPackViewSet, BarViewSet, JawViewSet

router = DefaultRouter()
router.register(r'hammers', VibratoryHammerViewSet)
router.register(r'clamps', ClampViewSet)
router.register(r'powerpacks', PowerPackViewSet)
router.register(r'bars', BarViewSet)
router.register(r'jaws', JawViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'rentals', RentalsViewSet)
router.register(r'components', ComponentViewSet)
router.register(r'customers/(?P<customer_id>\d+)/rentals', CustomerRentalViewSet, basename='customer-rentals')

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/', include(router.urls)),
    path('authenticate', check_authentication, name="check_authentication"),
    path('api/rentals/create/', CreateRentalConfigurationView.as_view(), name='create_rental'),

]
