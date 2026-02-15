from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DrinkRecordForm
from .models import DrinkRecord


@login_required
def drink_list(request):
    records = DrinkRecord.objects.filter(user=request.user).order_by('-recorded_date', '-id')
    return render(request, 'drink_app/drink_list.html',{"records": records})

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