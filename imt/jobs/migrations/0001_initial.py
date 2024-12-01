# Generated by Django 4.2 on 2024-12-01 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('skills', '0001_initial'),
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_on', models.DateField(auto_now_add=True)),
                ('comments', models.CharField(blank=True, max_length=250)),
                ('status', models.CharField(choices=[('O', 'Open'), ('P', 'In Progress'), ('C', 'Closed')], default='O', max_length=1)),
                ('final_result', models.CharField(choices=[('SJ', 'Selected Joined'), ('SNJ', 'Selected Did Not Join'), ('NS', 'Not Selected'), ('C', 'Cancelled'), ('P', 'Pending')], default='P', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='JobPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('job_company_id', models.CharField(max_length=10, unique=True)),
                ('min_exp_needed_in_years', models.PositiveIntegerField(default=0)),
                ('description', models.TextField()),
                ('optional_skills', models.ManyToManyField(blank=True, related_name='optional_for_positions', to='skills.skill')),
                ('required_skills', models.ManyToManyField(related_name='required_for_positions', to='skills.skill')),
            ],
        ),
        migrations.CreateModel(
            name='JobOpening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_date', models.DateField(auto_now_add=True)),
                ('closing_date', models.DateField()),
                ('job_type', models.CharField(choices=[('P', 'Permanent'), ('T', 'Temporary'), ('I', 'Intern')], default='P', max_length=1)),
                ('status', models.CharField(choices=[('O', 'Open'), ('C', 'Closed')], default='O', max_length=1)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_openings', to='jobs.jobposition')),
            ],
        ),
    ]
