from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "last_name", "first_name", "course", "year_level")
    search_fields = ("student_id", "first_name", "last_name", "email")
    list_filter = ("gender", "course", "year_level")