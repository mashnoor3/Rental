# Generated by Django 2.0.2 on 2018-03-23 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_ad_borrower'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='ad_img',
            field=models.ImageField(blank=True, default='catalog_images/no_img.png', null=True, upload_to='catalog_images'),
        ),
    ]
