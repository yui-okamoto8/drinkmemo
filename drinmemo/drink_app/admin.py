from django.contrib import admin
from .models import DrinkType, Ingredient, TasteFeature, DrinkRecord, DrinkRecordIngredient

admin.site.register(DrinkType)
admin.site.register(Ingredient)
admin.site.register(DrinkRecord)
admin.site.register(DrinkRecordIngredient)
admin.site.register(TasteFeature)
