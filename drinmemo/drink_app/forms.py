from django import forms
from .models import DrinkRecord
from .models import Ingredient

class DrinkRecordForm(forms.ModelForm):
    class Meta:
        model = DrinkRecord
        fields = [
            'image',
            'recorded_date',
            'drink_name',
            'drink_type',
            'store_name',
            'maker_name',
            'ingredients',
            'taste_rating',
            'total_rating',
            'memo',
        ]
        widgets = {
            'recorded_date': forms.DateInput(attrs={'type': 'date'}),
            'memo': forms.Textarea(attrs={'rows': 3}),
            'ingredients': forms.CheckboxSelectMultiple(attrs={'size':'8'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and getattr(self.instance, 'drink_type_id', None):
            self.fields['ingredients'].queryset = Ingredient.objects.filter(
                drink_type_id=self.instance.drink_type_id
            ).order_by('name')