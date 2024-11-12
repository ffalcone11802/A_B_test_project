#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A_B_test_project.settings')
django.setup()

from update_recs import UpdateRecs
import environ
env = environ.Env()
environ.Env.read_env()
update = UpdateRecs(config_path=env('CONFIG_PATH'))

def main():
    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Models initial update
    update.update_recs()

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
