from django.db.models import JSONField
from django.utils.text import slugify
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("category name"))
    slug = models.SlugField(max_length=150, null=False, blank=False, editable=False, verbose_name=_("category url"))
    parent = TreeForeignKey("self", on_delete=models.SET_NULL, related_name="children", null=True, blank=True,
                            verbose_name=_("parent category"), db_index=True)
    image = models.ImageField(upload_to='img/category/', null=True, blank=True)
    characteristic = JSONField(blank=True, null=True, default=dict)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('item category')
        verbose_name_plural = _('item categories')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    desc = models.CharField(max_length=500)
    image = models.ImageField(upload_to='img/item/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    characteristic = JSONField(blank=True, null=True, default=dict)

    def __str__(self):
        return self.title
