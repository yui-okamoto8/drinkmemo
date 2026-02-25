from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DrinkRecordForm, DrinkFilterForm
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Case, When, Value, IntegerField

from .models import DrinkRecord, Ingredient, TasteFeature, DrinkType


#記録一覧
@login_required
def drink_list(request):

    records = DrinkRecord.objects.filter(user=request.user).order_by('-recorded_date', '-id')
    
    query = request.GET.get('q') or ''
    start = request.GET.get('start') or ''
    end = request.GET.get('end') or ''
    drink_type = request.GET.get('drink_type') or ''
    taste = request.GET.get('taste') or ''
    total = request.GET.get('total') or ''

    ingredients_param = request.GET.get('ingredients') or ''
    taste_feature_ids = request.GET.getlist('taste_features')

    if query:
        records = records.filter(
            Q(drink_name__icontains=query) |
            Q(store_name__icontains=query) |
            Q(maker_name__icontains=query)
        )

    if start:
        records = records.filter(recorded_date__gte=start)
    if end:
        records = records.filter(recorded_date__lte=end)

    if drink_type:
        records = records.filter(drink_type_id=drink_type)

    if taste != '':
        records = records.filter(taste_rating=int(taste))

    if total != '':
        records = records.filter(total_rating=int(total))
    
    if ingredients_param:
        ids = [int(x) for x in ingredients_param.split(",") if x.isdigit()]
        if ids:
            records = records.filter(ingredients__id__in=ids).distinct()

    taste_feature_ids = request.GET.getlist('taste_features')
    ids = [int(x) for x in ingredients_param.split(",") if x.isdigit()]
    if taste_feature_ids:
        records = records.filter(taste_features__id__in=taste_feature_ids).distinct()

    records = records.order_by('-recorded_date', '-id')

    paginator = Paginator(records, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'drink_app/drink_list.html',{
        'records': records,
        'page_obj': page_obj,
        'q': query,
        'start': start,
        'end': end,
        'drink_type': drink_type,
        'taste': taste,
        'total': total,
        'ingredients': ingredients_param,
        'taste_features': taste_feature_ids,
        })


#記録画面
@login_required 
def drink_create(request):
    form = DrinkRecordForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            form.save_m2m()
            return redirect('drink_app:list')
        
    return render(request, 'drink_app/drink_form.html', {'form': form})


@login_required
def ingredients_filter(request):
    drink_type_id = request.GET.get('drink_type')
    if not drink_type_id:
        return JsonResponse({'ingredients': []})

    qs = Ingredient.objects.filter(drink_type_id=drink_type_id).annotate(
            is_other=Case(
                When(name='その他', then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('is_other', 'name')    
     
    data = [{'id': ing.id, 'name': ing.name} for ing in qs]
    return JsonResponse({'ingredients': data})


@login_required
def drink_detail(request, pk):
    record = get_object_or_404(DrinkRecord, pk=pk, user=request.user)
    return render(request, 'drink_app/drink_detail.html', {'record': record})


@login_required
def drink_update(request, pk):
    record = get_object_or_404(DrinkRecord, pk=pk, user=request.user)
    form = DrinkRecordForm(request.POST or None, request.FILES or None, instance=record)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('drink_app:detail', pk=record.pk)

    selected_ids = list(record.ingredients.values_list("id", flat=True))


    return render(request, 'drink_app/drink_form.html', {
        'form': form,
        'is_edit': True,
        'record':record,
        'selected_ids': selected_ids,
        })


@login_required
def drink_delete(request, pk):
    record = get_object_or_404(DrinkRecord, pk=pk, user=request.user)

    if request.method == 'POST':
        record.delete()
        return redirect('drink_app:list')

    return render(request, 'drink_app/drink_confirm_delete.html', {'record': record})

#フィルター
@login_required
def drink_filter(request):
    form = DrinkFilterForm(request.GET or None)
    return render(request, "drink_app/filter.html", {"form": form})

#集計
@login_required
def summary(request):
    base_qs = DrinkRecord.objects.filter(user=request.user)

    # よく飲む飲み物
    top_drink_type = (
        base_qs.values('drink_type__name')
        .annotate(cnt=Count('id'))
        .order_by('-cnt')
        .first()
    )

    # 好き/苦手：素材・味の特徴 上位3
    liked_qs = base_qs.filter(taste_rating=0)
    disliked_qs = base_qs.filter(taste_rating=2)

    top_like_ingredients = (
        Ingredient.objects.filter(drink_records__in=liked_qs)
        # .values('name')
        .exclude(name="その他")
        .annotate(cnt=Count('id'))
        .order_by('-cnt')[:3]
    )

    top_dislike_ingredients = (
        Ingredient.objects.filter(drink_records__in=disliked_qs)
        # .values('name')
        .exclude(name="その他")
        .annotate(cnt=Count('id'))
        .order_by('-cnt')[:3]
    )

    top_like_features = (
        TasteFeature.objects.filter(drink_records__in=liked_qs)
        .values('name')
        # .exclude(name="その他")
        .annotate(cnt=Count('id'))
        .order_by('-cnt')[:3]
    )

    top_dislike_features = (
        TasteFeature.objects.filter(drink_records__in=disliked_qs)
        .values('name')
        # .exclude(name="その他")
        .annotate(cnt=Count('id'))
        .order_by('-cnt')[:3]
    )

    return render(request, 'drink_app/summary.html', {
        'top_drink_type': top_drink_type,
        'top_like_ingredients': top_like_ingredients,
        'top_dislike_ingredients': top_dislike_ingredients,
        'top_like_features': top_like_features,
        'top_dislike_features': top_dislike_features,
    })