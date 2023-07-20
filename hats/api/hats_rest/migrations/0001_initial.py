# Generated by Django 4.0.3 on 2023-07-20 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BinVO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('closet_name', models.CharField(max_length=100)),
                ('bin_number', models.PositiveSmallIntegerField()),
                ('bin_size', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Hat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fabric', models.CharField(max_length=100)),
                ('style', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('picture_url', models.URLField()),
                ('wardrobe_location', models.CharField(max_length=100)),
            ],
        ),
    ]