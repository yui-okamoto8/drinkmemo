from django import forms
from .models import DrinkRecord
from .models import DrinkType, Ingredient, TasteFeature
from django.contrib.auth import get_user_model

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
            'taste_features',
            'total_rating',
            'memo',
        ]

        widgets = {
            'recorded_date': forms.DateInput(attrs={'type': 'date'}),
            'memo': forms.Textarea(attrs={'class':'form-control', 'rows': 3}),
            'ingredients': forms.CheckboxSelectMultiple(attrs={'size':'8'}),
            'taste_features': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['taste_features'].required = True

        if self.instance and getattr(self.instance, 'drink_type_id', None):
            self.fields['ingredients'].queryset = Ingredient.objects.filter(
                drink_type_id=self.instance.drink_type_id
            ).order_by('name')


TASTE_CHOICES = (
    ('', '指定なし'),
    ('0', '♡好き'),
    ('1', '⚪︎普通'),
    ('2', '×苦手'),
)

TOTAL_CHOICES = (
    ('', '指定なし'),
    ('0', '★★★'),
    ('1', '★★☆'),
    ('2', '★☆☆'),
    ('3', '☆☆☆'),
)

class DrinkFilterForm(forms.Form):

    start = forms.DateField(
        label='開始日', required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end = forms.DateField(
        label='終了日', required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    drink_type = forms.ModelChoiceField(
        label='飲み物の種類',
        queryset=DrinkType.objects.all(),
        required=False,
        empty_label='指定なし'
    )

    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all().order_by('name'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='素材',
    )

    taste = forms.ChoiceField(
        label='味の評価',
        choices=TASTE_CHOICES,
        required=False
    )

    taste_features = forms.ModelMultipleChoiceField(
        queryset=TasteFeature.objects.all().order_by('name'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='味の特徴'
    )

    total = forms.ChoiceField(
        label='総合評価',
        choices=TOTAL_CHOICES,
        required=False
    )

