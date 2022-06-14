# Generated by Django 4.0.4 on 2022-06-13 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AllAboutBookApp', '0005_remove_book_name_author_book_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='book',
        ),
        migrations.AddField(
            model_name='review',
            name='listread',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='AllAboutBookApp.listread'),
            preserve_default=False,
        ),
    ]
