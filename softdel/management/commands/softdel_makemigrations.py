from django.core.management.commands import makemigrations


class Command(makemigrations.Command):
    """Except handle unique """
    pass
