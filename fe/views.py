from django.shortcuts import render

# Create your views here.
def fe_index(request):
    return render(request, 'page/index.html')

def fe_upload(request):
    return render(request, 'page/upload_file.html')

def fe_review(request):
    return render(request, 'page/review_file.html')

def fe_wavelength(request):
    return render(request, 'page/wavelength.html')

def fe_materi(request):
    return render(request, 'page/materi.html')

def fe_quiz(request):
    return render(request, 'page/quiz.html')

def fe_indexv2(request):
    return render(request, 'page/v2/index.html')

def fe_uploadv2(request):
    return render(request, 'page/v2/upload.html')

def fe_reviewv2(request):
    return render(request, 'page/v2/review.html')

def fe_materiv2(request):
    return render(request, 'page/v2/materi.html')

def fe_quizv2(request):
    return render(request, 'page/v2/quiz.html')