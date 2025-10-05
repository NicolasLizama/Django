from django.shortcuts import render

# Create your views here.
def paginator(request):
    return render(request, 'pag.html')