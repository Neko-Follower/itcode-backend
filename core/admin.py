from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin

from core.models import Item, Category

# Register your models here.
admin.site.register(Item)
admin.site.register(Category, MPTTModelAdmin)