from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'index.html', {})


def about_us(request):
    return render(request, 'about.html', {'loc': 'about'})


def facilities(request):
    return render(request, 'facilities.html', {'loc': 'facilities'})


def under_const(request):
    return render(request, 'construction.html', {})