from django.shortcuts import render

def index(request):
    context = {
        'active_home': 'active'
    }
    return render(request, 'index.html', context)