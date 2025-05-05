from rest_framework import viewsets, filters
from .models import (
    Product,
    Page,
    ContactMessage,
    BlogCategory,
    BlogPost,
    BlogComment,
    FAQ,
)
from .serializers import (
    ProductSerializer,
    PageSerializer,
    ContactMessageSerializer,
    BlogCategorySerializer,
    BlogPostSerializer,
    BlogCommentSerializer,
    FAQSerializer,
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


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
