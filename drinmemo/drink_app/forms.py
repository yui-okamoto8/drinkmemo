from django import forms
from .models import DrinkRecord

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
        }
