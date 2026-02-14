from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def drink_list(request):
    return render(request, 'drink_app/drink_list.html')

