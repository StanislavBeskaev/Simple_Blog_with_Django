# Generated by Django 3.1.2 on 2021-02-27 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_title',
            field=models.CharField(default='', max_length=70, verbose_name='Заголовок поста'),
            preserve_default=False,
        ),
    ]
