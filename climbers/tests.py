from django.test import TestCase

from climbers.models import Climber


class MainTestCase(TestCase):

    test_password = 'testPasword'
    test_email = 'test@test.com'
    test_username = 'test_user'

    def test_create_climber(self):

        climber = Climber.objects.create_user(username=self.test_username, email=self.test_email, password=self.test_password, )
        self.assertEqual(climber.username, self.test_username)
        self.assertEqual(climber.email, self.test_email)
        self.assertNotEqual(climber.password, self.test_password)
        self.assertIsNotNone(climber.profile)
        self.assertIsNotNone(climber.preference)
        self.assertIsNotNone(climber.measurement)