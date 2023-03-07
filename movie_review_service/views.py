from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer
from django.shortcuts import render, redirect
import joblib
from .forms import ReviewForm
from django.http import HttpResponseRedirect
import os
from django.conf import settings




class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

def input_page(request):
    if request.method == 'POST':
        request_text = request.POST
        text_review = request_text['text']
        vec_path = os.path.join(settings.STATICFILES_DIRS[0], 'vectorizer.joblib')
        vectorizer = joblib.load(vec_path)
        pkl = os.path.join(settings.STATICFILES_DIRS[0], 'model_svm.pkl')
        clf = joblib.load(pkl)
        vectorizer_text = vectorizer.transform([text_review])
        pred = clf.predict(vectorizer_text)
        if pred > 5:
            emo = "Positive"
        else:
            emo = "Negative"
        rew = Review.objects.create(text=text_review, rating=pred[0], emotion=emo)
        rew.save()
        return redirect(reviews)
    return render(request, 'input_page.html')

def reviews(request):
    reviews = Review.objects.all().order_by('-id')
    return render(request, 'review.html', {'reviews': reviews})


