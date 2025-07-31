# your_app/models.py

from django.db import models
from django.utils.text import slugify

from PIL import Image
from django.core.files.base import ContentFile
import io


def resize_image(image_field, size=(800, 600), quality=75):
    from PIL import Image

    img = Image.open(image_field)
    img = img.convert("RGB")

    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.LANCZOS

    img.thumbnail(size, resample)

    buffer = io.BytesIO()
    name = image_field.name.rsplit("/", 1)[-1].split(".")[0]
    img.save(buffer, format="WEBP", quality=quality)

    return ContentFile(buffer.getvalue(), name=f"{name}.webp")


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Danh mục sản phẩm"
        verbose_name_plural = "Danh mục sản phẩm"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Danh mục",
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/", help_text="Size: 800 x 800px")
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Hình ảnh sản phẩm (Size: 800 x 800px)"
        verbose_name_plural = "Hình ảnh sản phẩm (Size: 800 x 800px)"

    def save(self, *args, **kwargs):
        # Resize nếu ảnh mới và chưa phải .webp
        if self.image and not self.image.name.endswith(".webp"):
            self.image = resize_image(self.image, size=(800, 800), quality=85)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} – Image #{self.sort_order}"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    variant_name = models.CharField(max_length=100)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Biến thể sản phẩm"
        verbose_name_plural = "Biến thể sản phẩm"

    def __str__(self):
        return f"{self.product.name} – {self.variant_name}"


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Đánh giá sản phẩm"
        verbose_name_plural = "Đánh giá sản phẩm"

    def __str__(self):
        return f"{self.user_name} - {self.product.name} ({self.rating}/5)"


class Page(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Trang tĩnh"
        verbose_name_plural = "Trang tĩnh"

    def __str__(self):
        return self.title


class GoogleServiceAccount(models.Model):
    name = models.CharField(max_length=100, default="default")
    credentials_file = models.FileField(upload_to="credentials/")
    spreadsheet_id = models.CharField(max_length=100, help_text="Google Sheet ID")

    def __str__(self):
        return self.name


class TrackingCode(models.Model):
    name = models.CharField(max_length=100)
    code = models.TextField()

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tin nhắn liên hệ"
        verbose_name_plural = "Tin nhắn liên hệ"

    def __str__(self):
        return f"{self.name} - {self.phone_number}"


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Chuyên mục"
        verbose_name_plural = "Chuyên mục"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(
        upload_to="blog/", blank=True, null=True, help_text="Size: 450 x 450px"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Tự sinh từ tiêu đề, bỏ dấu và chuyển sang ASCII",
    )
    content = models.TextField()
    author_name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(null=True, blank=True)
    categories = models.ManyToManyField(BlogCategory, related_name="posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Bài viết"
        verbose_name_plural = "Bài viết"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.thumbnail and not self.thumbnail.name.endswith(".webp"):
            self.thumbnail = resize_image(self.thumbnail, size=(450, 450), quality=80)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="comments"
    )
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Bình luận"
        verbose_name_plural = "Bình luận"

    def __str__(self):
        return f"{self.user_name} on {self.post.title}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class ContactInfo(models.Model):
    STATUS_CHOICES = [
        ("location", "Location"),
        ("email", "Email"),
        ("phone", "Phone"),
        ("facebook", "Facebook"),
        ("tiktok", "Tiktok"),
        ("instagram", "Instagram"),
        ("zalo", "Zalo"),
    ]
    type = models.CharField(max_length=20, choices=STATUS_CHOICES, default="location")
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="contact/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"

    class Meta:
        verbose_name = "Thông tin liên hệ"
        verbose_name_plural = "Thông tin liên hệ"


class Slide(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="slides/", help_text="Size: 1920 x 742 px")
    link = models.URLField(blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Slide"
        verbose_name_plural = "Slides"

    def save(self, *args, **kwargs):
        # Resize ảnh trước khi lưu
        if self.image and not self.image.name.endswith(".webp"):
            self.image = resize_image(self.image, size=(1920, 742), quality=85)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class WebsiteInfomation(models.Model):
    title = models.CharField(max_length=255, default="default")
    description = models.CharField(max_length=255, blank=True)
    thumbnail = models.ImageField(
        upload_to="thumbnail/", blank=True, null=True, help_text="Size: 1200 x 630 px"
    )
    url = models.CharField(max_length=255, blank=True)
    siteName = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Thông tin website"
        verbose_name_plural = "Thông tin website"

    def save(self, *args, **kwargs):
        if self.thumbnail and not self.thumbnail.name.endswith(".webp"):
            self.thumbnail = resize_image(self.thumbnail, size=(1200, 630), quality=85)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
