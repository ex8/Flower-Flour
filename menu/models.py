from django.db import models
from django.core.urlresolvers import reverse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_resized import ResizedImageField
from django.core.files.base import ContentFile
from resizeimage import resizeimage


class Menu(models.Model):
    banner_image = models.ImageField(upload_to='menu')

    class Meta:
        verbose_name = 'menu'

    def __str__(self):
        return "Menu Config"


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu:menu_list_by_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='products', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='products')
    sort = models.PositiveIntegerField(default=9999)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu:menu_detail', args=[self.id, self.slug])

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     pil_img = Image.open(self.image)
    #     new_image = resizeimage.resize(method='cover', image=pil_img, size=[400, 400])
    #     new_image_io = BytesIO()
    #     new_image.save(new_image_io, format='PNG')
    #     temp_name = self.image.name
    #     self.image.delete(save=False)
    #     self.image.save(
    #         temp_name,
    #         content=ContentFile(new_image_io.getvalue()),
    #         save=False
    #     )
    #     super(Product, self).save()
