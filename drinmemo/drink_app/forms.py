from django import forms
from .models import DrinkRecord

class DrinkRecordForm(forms.ModelForm):
    class Meta:
        model = DrinkRecord
        fields = [
            'recorded_date',
            'drink_name',
            'store_name',
            'maker_name',
            'taste_rating',
            'total_rating',
            'memo',
            'image',
            'ingredients',
        ]
        widgets = {
            'recorded_date': forms.DateInput(attrs={'type': 'date'}),
            'memo': forms.Textarea(attrs={'rows': 3}),
        }
