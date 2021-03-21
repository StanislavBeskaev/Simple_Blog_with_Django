# Generated by Django 3.1.2 on 2021-02-27 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileAvatarImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar_image_file', models.ImageField(upload_to='avatar_images/', verbose_name='картинка, аватар профиля пользователя')),
            ],
        ),
    ]