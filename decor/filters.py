# filters.py
from django_filters import rest_framework as filters
from .models import BlogPost


class BlogPostFilter(filters.FilterSet):
    categories = filters.BaseInFilter(field_name="categories__slug", lookup_expr="in")

    class Meta:
        model = BlogPost
        fields = ["categories"]
