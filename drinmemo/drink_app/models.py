from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DrinkType(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'drink_types'

class Ingredient(TimeStampedModel):
    drink_type = models.ForeignKey(DrinkType, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ingredients'


class DrinkRecord(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='drink_records')
    recorded_date = models.DateField('記録日')
    drink_name = models.CharField('飲み物名', max_length=100)
    store_name = models.CharField('店舗名', max_length=100, blank=True, null=True)
    maker_name = models.CharField('メーカー名', max_length=100, blank=True, null=True)
    TASTE_CHOICES = ((0, '好き'), (1, '普通'), (2, '苦手'))
    taste_rating = models.IntegerField('味の評価', choices=TASTE_CHOICES)
    total_rating = models.IntegerField('総合評価')
    memo = models.TextField('メモ', blank=True, null=True)
    image = models.ImageField('写真', upload_to='drink_records/', blank=True, null=True)

    drink_type = models.ForeignKey(
    DrinkType,
    on_delete=models.PROTECT,
    related_name="drink_records",
    verbose_name='飲み物の種類',
    )
    
    ingredients = models.ManyToManyField(
    Ingredient,
    through="DrinkRecordIngredient",
    related_name='drink_records',
    verbose_name='素材',
    )

    class Meta:
        db_table = 'drink_records'
    
class DrinkRecordIngredient(TimeStampedModel):
    drink_record = models.ForeignKey(DrinkRecord, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)

    class Meta:
        db_table = 'drink_record_ingredients'
        constraints = [
            models.UniqueConstraint(fields=["drink_record", "ingredient"], name="uniq_record_ingredient")
        ]