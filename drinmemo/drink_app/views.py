from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DrinkRecordForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Ingredient
from .forms import DrinkFilterForm
from django.urls import reverse
from urllib.parse import urlencode


from .models import DrinkRecord


@login_required
def drink_list(request):

    records = DrinkRecord.objects.filter(user=request.user).order_by('-recorded_date', '-id')
    
    query = request.GET.get('q') or ''
    start = request.GET.get('start') or ''
    end = request.GET.get('end') or ''
    drink_type = request.GET.get('drink_type') or ''
    taste = request.GET.get('taste') or ''
    total = request.GET.get('total') or ''

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

    records = records.order_by('-recorded_date', '-id')

    paginator = Paginator(records, 3)
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
        })


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

    qs = Ingredient.objects.filter(drink_type_id=drink_type_id).order_by('name')
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

@login_required
def drink_filter(request):
    form = DrinkFilterForm(request.GET or None)

    if request.GET.get('submit'):
        if form.is_valid():  
            params = {}

            start = form.cleaned_data.get('start')
            if start:
                params['start'] = start.strftime('%Y-%m-%d')

            end = form.cleaned_data.get('end')
            if end:
               params['end'] = end.strftime('%Y-%m-%d')

            drink_type = form.cleaned_data.get('drink_type')
            if drink_type:
                params['drink_type'] = str(drink_type.id)

            taste = form.cleaned_data.get('taste')
            if taste != '':
                params['taste'] = taste

            total = form.cleaned_data.get('total')
            if total != '':
                params['total'] = total

            url = reverse('drink_app:list')
            if params:
              url = f'{url}?{urlencode(params)}'
            return redirect(url)

    return render(request, 'drink_app/filter.html', {'form': form})
