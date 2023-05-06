from django.test import TestCase
from .models import Role


class DeleteTest(TestCase):

    def test_delete(self):
        role = Role.objects.create()
        c1 = Role.objects.count()

        role.delete()
        c2 = Role.objects.count()
        self.assertEqual(c1 - 1, c2)

        c3 = Role.base_objects.count()  # use django objects
        self.assertEqual(c1, c3)
