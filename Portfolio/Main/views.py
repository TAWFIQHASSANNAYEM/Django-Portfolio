from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Experience, Education, Project, ContactMessage
from django.contrib import messages
from django.core.mail import send_mail


def home_view(request):
    return render(request, "home.html")

def home_view(request):
    profile = Profile.objects.first()  
    experiences = Experience.objects.order_by("-start_date")
    educations = Education.objects.order_by("-end_year")
    featured_projects = Project.objects.filter(is_featured=True)
    all_projects = Project.objects.all()

    context = {
        "profile": profile,
        "experiences": experiences,
        "educations": educations,
        "featured_projects": featured_projects,
        "all_projects": all_projects,
    }
    return render(request, "home.html", context)

def home_view(request):
    profile = Profile.objects.first()
    experiences = Experience.objects.order_by("-start_date")
    educations = Education.objects.order_by("-end_year")
    featured_projects = Project.objects.filter(is_featured=True)
    all_projects = Project.objects.all()
    
    context = {
        "profile": profile,
        "experiences": experiences,
        "educations": educations,
        "featured_projects": featured_projects,
        "all_projects": all_projects,
    }
    return render(request, "home.html", context)

def about_view(request):
    profile = Profile.objects.first()
    educations = Education.objects.all()
    context = {"profile": profile, "educations": educations}
    return render(request, "about.html", context)

def experience_view(request):
    experiences = Experience.objects.order_by("-start_date")
    educations = Education.objects.order_by("-end_year")
    context = {"experiences": experiences, "educations": educations}
    return render(request, "experience.html", context)

def projects_view(request):
    projects = Project.objects.all()
    featured_projects = Project.objects.filter(is_featured=True)
    context = {"projects": projects, "featured_projects": featured_projects}
    return render(request, "projects.html", context)

def contact_view(request):
    profile = Profile.objects.first()
    
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            subject=request.POST["subject"],
            message=request.POST["message"],
        )
        messages.success(request, "Message sent successfully! I'll get back to you soon.")
        return redirect("contact")
    
    context = {"profile": profile}
    return render(request, "contact.html", context)
