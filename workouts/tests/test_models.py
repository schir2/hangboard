from django.test import TestCase

from climbers.models import Climber

from workouts.models import Hold
from workouts.models import Hangboard
from workouts.models import Material
from workouts.models import HoldType
from workouts.models import Workout
from workouts.models import WorkoutSet
from workouts.models import Exercise


# Create your tests here.

class MainTestCase(TestCase):

    def create_climber(self):
        return Climber.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='testPassword!',
        )

    def setUp(self):
        self.climber = self.create_climber()
        self.material = Material.objects.create_object(
            name='Test Material',
            climber=self.climber,
        )
        self.hangboard = Hangboard.objects.create(
            name='Test Hangboard',
            climber=self.climber,
            material=self.material,
        )
        self.exercise = Exercise.objects.create(name='Pull Up', climber=self.climber)
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

        self.workout = Workout.objects.add_workout(
            name='Pull Up Pyramid',
            climber=self.climber,
            hangboard=self.hangboard,
        )

    def test_hold_type_equality(self):
        self.assertTrue(self.left_crimp.is_same_type(self.right_crimp))
        self.assertTrue(not self.left_crimp.is_same_type(self.left_jug))
        self.assertTrue(not self.left_jug.is_same_type(self.right_sloper))
        self.assertTrue(self.left_crimp.is_same_type(self.left_crimp))

    def test_workout_set_manager(self):
        first_workout_set = WorkoutSet.objects.add_workout_set(
            climber=self.climber,
            exercise=self.exercise,
            workout=self.workout,
            left_fingers=0,
            right_hold=self.right_sloper,
            right_fingers=self.right_sloper.max_fingers,

        )

        second_workout_set = WorkoutSet.objects.add_workout_set(
            climber=self.climber,
            exercise=self.exercise,
            workout=self.workout,
            previous=first_workout_set,
            left_fingers=0,
            right_hold=self.left_crimp,
            right_fingers=self.right_sloper.max_fingers,

        )

        third_workout_set = WorkoutSet.objects.add_workout_set(
            climber=self.climber,
            exercise=self.exercise,
            workout=self.workout,
            previous=second_workout_set,
            left_fingers=0,
            right_hold=self.left_jug,
            right_fingers=self.right_sloper.max_fingers,
        )

        workout_sets = self.workout.get_workout_sets()
        for workout_set in workout_sets:
            print(workout_set)

        self.assertEqual(
            first_workout_set.previous,
            None,
            'first_workout_set.previous should be set to None'
        )

        self.assertEqual(
            second_workout_set.previous,
            first_workout_set,
            'second_workout_set.previous should be first_workout_set'
        )

        self.assertEqual(
            third_workout_set.previous,
            second_workout_set,
            'third_workout_set.previous should be equal to second_workout_set'
        )

        second_workout_set.delete()
        third_workout_set = WorkoutSet.objects.get(pk=third_workout_set.pk)

        self.assertEqual(
            third_workout_set.previous,
            first_workout_set,
            'third_workout_set.previous should be first_workout_set after deletion'
        )

        first_workout_set.delete()
        third_workout_set = WorkoutSet.objects.get(pk=third_workout_set.pk)

        self.assertEqual(
            third_workout_set.previous,
            None,
            'third_workout_set.previous should be None after deletion'
        )
