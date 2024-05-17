from django.shortcuts import render
from django.http import HttpResponse
from .models import Price, Discount
# Create your views here.
def index(request):
    producs = Price.objects.all()
    print(producs)
    return render(request, "index.html", {
        "products":producs
    })