from django.test import TestCase
from .models import Role, User


class ForeignKeyTest(TestCase):

    def test_cascade(self):
        role = Role.objects.create()
        User.objects.create(role=role)
        c1 = User.objects.count()

        role.delete()
        c2 = User.objects.count()
        self.assertEqual(c1 - 1, c2)

    def test_relation(self):
        role = Role.objects.create()
        user = User.objects.create(role=role)
        self.assertEqual(role.user_set.count(), 1)

        user.delete()
        self.assertEqual(role.user_set.count(), 0)
