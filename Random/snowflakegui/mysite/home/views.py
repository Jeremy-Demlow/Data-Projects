from django.shortcuts import render


def profile_index(request):
    return render(request, 'profile_index.html', {})


def contact_index(request):
    return render(request, 'contact.html', {})


def about_index(request):
    return render(request, 'about.html', {})


def pricing_index(request):
    return render(request, 'pricing.html', {})


def tutorials_index(request):
    return render(request, 'tutorials.html', {})


def home_index(request):
    return render(request, 'home.html', {})
