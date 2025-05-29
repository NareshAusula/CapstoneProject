from django.contrib import admin
from .models import CarMake, CarModel


#CarModelInline  Allows editing CarModel entries directly within the CarMake admin page.
class CarModelInline(admin.StackedInline):  #Displays fields vertically (use TabularInline for a compact table).
    model = CarModel
    extra = 1

#Model-Specific Settings
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')  #Fields shown in the list view (e.g., "Camry | Toyota | Sedan | 2023").
    list_filter = ('car_make', 'type', 'year')           #Adds filters on the right (filter by make, type, or year).
    search_fields = ('name', 'car_make__name')           #Enables search by model name or make name (car_make__name).

#(Parent Model + Inlines
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
