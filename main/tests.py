from django.test import TestCase
from main.models import Hold
from main.models import Hangboard
from climbers.models import Climber
from main.models import Material
from main.models import HoldType
from main.models import Workout

# Create your tests here.

class MainTestCase(TestCase):

    def setUp(self):
        self.climber = Climber.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='testPassword!',
        )
        self.material = Material.objects.create_object(
            name='Test Material',
            climber=self.climber,
        )
        print(self.material)
        self.hangboard = Hangboard.objects.create(
            name='Test Hangboard',
            climber=self.climber,
            material=self.material,
        )
        self.crimp = HoldType.objects.create(name='Test Crimp', climber=self.climber)
        self.jug = HoldType.objects.create(name='Test Jug', climber=self.climber)
        self.sloper = HoldType.objects.create(name='Test Sloper', climber=self.climber)
        self.left_crimp = Hold.objects.create(
            name='Test Left Crimp',
            climber=self.climber,
            hangboard=self.hangboard,
            hold_type=self.crimp,
            position_id=1,
            size=20,
            max_fingers=4,
            position='L',
        )
        self.right_crimp = Hold.objects.create(
            name='Test Right Crimp',
            climber=self.climber,
            hangboard=self.hangboard,
            hold_type=self.crimp,
            position_id=2,
            size=20,
            max_fingers=4,
            position='R',
        )
        self.left_jug = Hold.objects.create(
            name='Test Left Jug',
            climber=self.climber,
            hangboard=self.hangboard,
            hold_type=self.jug,
            position_id=3,
            max_fingers=4,
            position='L'
        )
        self.right_sloper = Hold.objects.create(
            name='Test Right Sloper',
            climber=self.climber,
            hangboard=self.hangboard,
            hold_type=self.sloper,
            position_id=4,
            size=20,
            angle=20,
            max_fingers=4,
            position='M',
        )

    def test_hold_type_equality(self):
        self.assertTrue(self.left_crimp.is_same_type(self.right_crimp))
        self.assertTrue(not self.left_crimp.is_same_type(self.left_jug))
        self.assertTrue(not self.left_jug.is_same_type(self.right_sloper))
        self.assertTrue(self.left_crimp.is_same_type(self.left_crimp))

    def test_create_workout(self):
        self.workout = Workout.objects.create_workout(
            name='Pull Up Pyramid',
            climber=self.climber,
            hangboard=self.hangboard,
        )
        print(self.workout, self.workout.slug)