from django.contrib import admin
from .models import Product,Department,Profile,Order1,DeliveryDetail,OrderProduct,Review

admin.site.register(Product)
admin.site.register(Department)
admin.site.register(Profile)
admin.site.register(DeliveryDetail)
admin.site.register(OrderProduct)
# admin.site.register(Order)
admin.site.register(Review)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct

@admin.register(Order1)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]