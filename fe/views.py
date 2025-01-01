from django.shortcuts import render

# Create your views here.
def fe_index(request):
    return render(request, 'page/index.html')

def fe_upload(request):
    return render(request, 'page/upload_file.html')

def fe_review(request):
    return render(request, 'page/review_file.html')