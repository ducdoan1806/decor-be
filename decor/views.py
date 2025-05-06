from rest_framework import viewsets, filters
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/products/?category=<slug>&search=<term>&ordering=<field>&page=<n>
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "category__slug"]
    ordering_fields = ["price", "created_at"]


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "email", "subject", "message"]


class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(status="published")
    serializer_class = BlogPostSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content", "author_name"]


class BlogCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["user_name", "user_email", "comment"]


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["question", "answer"]


class ContactInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer


class SlideViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer
