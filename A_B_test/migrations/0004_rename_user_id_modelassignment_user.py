# Generated by Django 5.1.1 on 2024-10-04 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('A_B_test', '0003_alter_modelassignment_recommendations_model_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelassignment',
            old_name='user_id',
            new_name='user',
        ),
    ]