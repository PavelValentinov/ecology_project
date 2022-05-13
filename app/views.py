from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Index templates
def index(request):
    return render(request, 'index.html')

# Company selection templates
def company_selection(request):
    return render(request, 'company_selection.html')

# Company verification selection templates
def company_verification(request):
    return render(request, 'company_verification.html')

# Contacts templates
def contacts(request):
    return render(request, 'contacts.html')