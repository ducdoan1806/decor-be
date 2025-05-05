# your_app/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import *
from django import forms
from ckeditor.widgets import CKEditorWidget  # nếu đã cài ckeditor
from slugify import slugify

# --- Product Admin ---


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "image_preview", "alt_text", "sort_order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Preview"


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductReviewInline(admin.StackedInline):
    model = ProductReview
    extra = 0
    readonly_fields = ("user_name", "rating", "comment", "created_at")
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductVariantInline, ProductReviewInline]
    prepopulated_fields = {"slug": ("name",)}


# --- Page Admin ---


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)


# --- ContactMessage Admin ---


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    ordering = ("-created_at",)


# --- Blog Admin ---


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ("user_name", "user_email", "comment", "created_at")
    can_delete = False


class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = BlogPost
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        slug = cleaned_data.get("slug")
        if not slug and title:
            cleaned_data["slug"] = slugify(title, allow_unicode=True)
        return cleaned_data


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author_name", "status", "published_at")
    list_filter = ("status", "published_at")
    search_fields = ("title", "content", "author_name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    inlines = [BlogCommentInline]
    form = BlogPostForm


# --- FAQ Admin ---


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "sort_order")
    list_editable = ("sort_order",)
    ordering = ("sort_order",)
