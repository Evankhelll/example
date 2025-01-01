from django.shortcuts import render

# Create your views here.
def publik_index_view(request):
    return render(request, 'publik/profil/index.html')