from django.contrib import admin
from .models import JobApplication, JobOpening, JobPosition


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ("applied_on", "candidate")
    list_display = ("candidate", "applied_on", "status", "final_result")


@admin.register(JobOpening)
class JobopeningAdmin(admin.ModelAdmin):
    readonly_fields = ("posted_date",)
    list_display = ("position", "posted_date", "closing_date", "job_type", "status")


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "job_company_id",
    )
