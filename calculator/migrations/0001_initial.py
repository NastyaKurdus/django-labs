# Generated by Django 3.2 on 2021-05-15 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Calculator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('mode', models.CharField(choices=[('S', 'Standard'), ('P', 'Programmer')], max_length=1)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calculators', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_time',),
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('expr', models.TextField()),
                ('result', models.TextField()),
                ('calculator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_items', to='calculator.calculator')),
            ],
            options={
                'ordering': ('created_time',),
                'abstract': False,
            },
        ),
    ]
