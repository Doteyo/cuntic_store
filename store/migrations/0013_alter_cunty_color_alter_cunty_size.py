# Generated by Django 4.2.5 on 2023-09-15 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_message_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cunty',
            name='color',
            field=models.CharField(default='', max_length=30, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='cunty',
            name='size',
            field=models.CharField(default='', max_length=3, verbose_name='Размер'),
        ),
    ]
