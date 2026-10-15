from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Student


def signup(request):
    if request.user.is_authenticated:
        return redirect("student_list")

    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account was created successfully.")
        return redirect("student_list")

    return render(request, "tostos_sahur/signup.html", {"form": form})


@login_required
def student_list(request):
    search_query = request.GET.get("q", "").strip()
    students = Student.objects.all()
    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(student_id__icontains=search_query)
            | Q(course__icontains=search_query)
            | Q(year_level__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(contact_number__icontains=search_query)
        )
    return render(
        request,
        "tostos_sahur/student_list.html",
        {"students": students, "search_query": search_query},
    )


@login_required
def student_create(request):
    if request.method == "POST":
        Student.objects.create(
            student_id=request.POST["student_id"],
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            age=request.POST["age"],
            gender=request.POST["gender"],
            course=request.POST["course"],
            year_level=request.POST["year_level"],
            email=request.POST["email"],
            contact_number=request.POST["contact_number"],
        )
        messages.success(request, "Student record added successfully.")
        return redirect("student_list")
    return render(request, "tostos_sahur/student_form.html", {"title": "Add Student"})


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        for field in ("student_id", "first_name", "last_name", "age", "gender", "course", "year_level", "email", "contact_number"):
            setattr(student, field, request.POST[field])
        student.save()
        messages.success(request, "Student record updated successfully.")
        return redirect("student_list")
    return render(request, "tostos_sahur/student_form.html", {"title": "Edit Student", "student": student})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student record removed successfully.")
        return redirect("student_list")
    return render(request, "tostos_sahur/student_confirm_delete.html", {"student": student})
