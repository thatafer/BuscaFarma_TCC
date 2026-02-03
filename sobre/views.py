from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def sobre(request):
   if request.method == 'GET':
      return render(request, 'sobre.html')
   
def programadores(request):
   return render(request, 'programadores.html')

def sistema(request):
   return render(request, 'sistema.html')