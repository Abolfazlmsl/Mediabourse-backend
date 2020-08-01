from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Watcher)
admin.site.register(Stock)
admin.site.register(Orders)
admin.site.register(Cart)
