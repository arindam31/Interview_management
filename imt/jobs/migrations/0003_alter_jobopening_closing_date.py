# Generated by Django 4.2 on 2024-12-06 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobopening',
            name='closing_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
