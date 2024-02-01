from django.shortcuts import render

def cadastro_view(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')