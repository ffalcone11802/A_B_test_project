#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A_B_test_project.settings')
os.environ.setdefault('TF_ENABLE_ONEDNN_OPTS', '0')
django.setup()


def main():
    # Models initial training
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        from A_B_test.recs_manager import RecsManager
        import A_B_test.test_config as config
        config.recs_manager = RecsManager(config_path=config.config_path)
        config.recs_manager.update_recs()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
