from django.contrib import admin

from vehicles.models import Vehicle, VehicleImages

admin.site.register(VehicleImages)

class VehicleImagesInline(admin.TabularInline):
    model = VehicleImages
    extra = 1

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "brand", "model", "year","price_per_hour", "price_per_day", "is_available")
    inlines = [VehicleImagesInline]


