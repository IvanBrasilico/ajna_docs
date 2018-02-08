#!/usr/bin/env python
import os
print('teste')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ajna.settings")
print('teste2')
try:
    from django.core.management import execute_from_command_line
except ImportError:
    # The above import may fail for some other reason. Ensure that the
    # issue is really that Django is missing to avoid masking other
    # exceptions on Python 2.
    try:
        import django
    except ImportError:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    raise
argv = ['manage.py', 'runserver']
print('teste3')
execute_from_command_line(argv)
