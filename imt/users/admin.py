from django.contrib import admin
from .models import User, Candidate


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("username", "created_at", "updated_at", "is_active", "is_staff")


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "city")
