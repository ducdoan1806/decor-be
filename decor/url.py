# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"pages", PageViewSet)
router.register(r"contacts", ContactMessageViewSet, basename="contactmessage")
router.register(r"blog/categories", BlogCategoryViewSet)
router.register(r"blog/posts", BlogPostViewSet)
router.register(r"blog/comments", BlogCommentViewSet)
router.register(r"faqs", FAQViewSet)
router.register(r"contact-info", ContactInfoViewSet)
router.register(r"slide", SlideViewSet)
router.register(r"tracking-codes", TrackingCodeViewSet, basename="trackingcode")

urlpatterns = [
    path("", include(router.urls)),
]
