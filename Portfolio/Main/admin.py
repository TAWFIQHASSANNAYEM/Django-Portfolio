from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Profile, Experience, Education, Project , ContactMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "headline", "email", "updated_at")
    list_editable = ("headline",)
    search_fields = ("full_name", "email")
    readonly_fields = ("updated_at",)
    
    fieldsets = (
        ("Profile Info", {
            "fields": ("full_name", "headline", "location", "email", "phone", "linkedin_url", "github_url", "facebook_url", "instagram_url", "cv_file")
        }),
        ("About", {
            "fields": ("about",)
        }),
        ("Image", {
            "fields": ("profile_image",),
            "classes": ("collapse",)
        }),
        ("Timestamps", {
            "fields": ("updated_at",),
            "classes": ("collapse",)
        }),
    )
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%;"/>',
                obj.profile_image.url
            )
        return "No image"
    profile_image_preview.short_description = "Profile Image"


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "organization", "start_date_formatted", "end_date_formatted", "is_current")
    list_filter = ("organization", "is_current", "start_date")
    search_fields = ("role", "organization", "description")
    list_editable = ("is_current",)
    date_hierarchy = "start_date"
    
    fieldsets = (
        ("Position", {
            "fields": ("role", "organization", "location")
        }),
        ("Dates", {
            "fields": ("start_date", "end_date", "is_current")
        }),
        ("Description", {
            "fields": ("description",),
            "classes": ("monospace",)
        }),
    )
    
    def start_date_formatted(self, obj):
        return obj.start_date.strftime("%b %Y")
    start_date_formatted.short_description = "Start"
    start_date_formatted.admin_order_field = "start_date"
    
    def end_date_formatted(self, obj):
        if obj.is_current:
            return "Present"
        if obj.end_date:
            return obj.end_date.strftime("%b %Y")
        return "-"
    end_date_formatted.short_description = "End"
    end_date_formatted.admin_order_field = "end_date"


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "years_display", "result_or_cgpa")
    list_filter = ("institution", "start_year")
    search_fields = ("degree", "institution", "field_of_study")
    ordering = ("-end_year",)
    
    fieldsets = (
        ("Education", {
            "fields": ("institution", "degree", "field_of_study")
        }),
        ("Details", {
            "fields": ("start_year", "end_year", "result_or_cgpa")
        }),
        ("Description", {
            "fields": ("description",),
            "classes": ("monospace",)
        }),
    )
    
    def years_display(self, obj):
        return f"{obj.start_year}–{obj.end_year}"
    years_display.short_description = "Years"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "tech_stack_short", "created_at")
    list_filter = ("is_featured", "created_at")
    list_editable = ("is_featured",)
    search_fields = ("title", "short_description", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "image_preview")
    
    fieldsets = (
        ("Project Info", {
            "fields": ("title", "slug", "is_featured")
        }),
        ("Description", {
            "fields": ("short_description", "long_description")
        }),
        ("Tech & Links", {
            "fields": ("tech_stack", "github_url", "live_url")
        }),
        ("Image", {
            "fields": ("image", "image_preview"),
            "classes": ("collapse",)
        }),
        ("Timestamps", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )
    
    def tech_stack_short(self, obj):
        return obj.tech_stack[:50] + "..." if len(obj.tech_stack) > 50 else obj.tech_stack
    tech_stack_short.short_description = "Tech Stack"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 150px; height: 100px; object-fit: cover;"/>',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Project Image"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)
    actions = ["mark_as_read", "mark_as_unread"]
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected as unread"
