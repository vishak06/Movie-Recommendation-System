from django.shortcuts import render
from django.http import JsonResponse
from .similarity import movie_recommendation, get_movie_suggestions

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

def autocomplete(request):
    """
    API endpoint for movie autocomplete suggestions
    """
    query = request.GET.get('q', '')
    suggestions = get_movie_suggestions(query, limit=4)
    return JsonResponse({'suggestions': suggestions})
