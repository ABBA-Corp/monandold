# Generated by Django 4.1 on 2022-08-29 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0003_about_partner_name_en_partner_name_ru_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='name_ru',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='name_uz',
        ),
        migrations.AlterField(
            model_name='partner',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
