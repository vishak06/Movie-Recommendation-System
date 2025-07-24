from django.shortcuts import render
from .similarity import movie_recommendation

# Create your views here.
def index(request):
    recommendation = []
    if request.method == 'POST':
        title = request.POST.get('title')
        number = int(request.POST.get('number'))
        recommendation = movie_recommendation(title, number)

    return render(request, 'recommendation/movies.html', {
        'recommendation' : recommendation
    })
