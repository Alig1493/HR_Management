import factory
from django.contrib.auth import get_user_model
from factory.django import ImageField
from factory.fuzzy import FuzzyChoice
from faker import Faker

from hr.users.config import Config

fake = Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.LazyAttribute(lambda o: '%s@misfit.tech' % o.name.replace(" ", "."))
    role = FuzzyChoice([obj[0] for obj in Config.CHOICES])
    profile_image = ImageField(filename="new_image.jpg")
    password = factory.PostGenerationMethodCall('set_password', 'test_pass')
