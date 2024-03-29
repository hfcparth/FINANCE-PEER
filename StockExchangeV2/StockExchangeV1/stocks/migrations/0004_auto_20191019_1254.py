# Generated by Django 2.2.6 on 2019-10-19 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stocks', '0003_auto_20191019_1227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='seller_email',
            new_name='seller',
        ),
        migrations.CreateModel(
            name='Buyorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('buy_value', models.FloatField()),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
