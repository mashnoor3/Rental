# Generated by Django 2.0.2 on 2018-03-19 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_profile_favourites'),
        ('catalog', '0019_auto_20180318_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrower', to='profiles.Profile'),
        ),
    ]
