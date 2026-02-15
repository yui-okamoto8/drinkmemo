from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DrinkRecordForm
from django.db.models import Q
from django.core.paginator import Paginator

from .models import DrinkRecord


@login_required
def drink_list(request):
    query = request.GET.get('q')

    records = DrinkRecord.objects.filter(user=request.user).order_by('-recorded_date', '-id')
    
    if query:
        records = records.filter(
            Q(drink_name__icontains=query) |
            Q(store_name__icontains=query) |
            Q(maker_name__icontains=query)
        )
  
    paginator = Paginator(records, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'drink_app/drink_list.html',{
        'records': records,
        'page_obj': page_obj,
        'q': query,
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