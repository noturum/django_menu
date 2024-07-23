# Generated by Django 5.0.7 on 2024-07-23 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('named_url', models.CharField(blank=True, max_length=200, null=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='menu_app.menu')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menu_app.menuitem')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('menu', 'parent', 'order')},
            },
        ),
    ]
