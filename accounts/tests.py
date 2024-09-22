from django.test import TestCase

from .models import  VibratoryHammer,RentalConfiguration
# Create your tests here.


class VibratoryHammerModelTest(TestCase):

    def test_string_serial_num(self):
        hammer= VibratoryHammer(serial_number="22X001")

        self.assertEqual(str(hammer),hammer.serial_number)





class RentalConfigurationModelTest(TestCase):

    def test_string_serial_num(self):
        rental= RentalConfiguration()

        self.assertEqual(str(rental),"Rentals")
