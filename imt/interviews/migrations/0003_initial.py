# Generated by Django 4.2 on 2024-12-05 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('interviews', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewround',
            name='interviewers',
            field=models.ManyToManyField(blank=True, related_name='interview_rounds', to='users.staff'),
        ),
        migrations.AddField(
            model_name='interviewround',
            name='next_round',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prev_round', to='interviews.interviewround'),
        ),
        migrations.AddField(
            model_name='interviewfeedback',
            name='interviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_entries', to='users.staff'),
        ),
        migrations.AddField(
            model_name='interviewfeedback',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_entries', to='interviews.interviewround'),
        ),
        migrations.AlterUniqueTogether(
            name='interviewfeedback',
            unique_together={('round', 'interviewer')},
        ),
    ]
