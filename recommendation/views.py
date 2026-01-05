from django.shortcuts import render
from django.http import JsonResponse
from .similarity import movie_recommendation, get_movie_suggestions

# Create your views here.
def index(request):
    recommendation = []
    # Check for title in GET or POST
    title = request.GET.get('title') or request.POST.get('title')
    movie_index = request.GET.get('movie_index') or request.POST.get('movie_index')
    
    if title:
        number = request.GET.get('number') or request.POST.get('number')
        # Default to 10 if number is missing/invalid, though HTML enforces it.
        # It's safer to handle conversion errors
        try:
            number = int(number)
        except (ValueError, TypeError):
            number = 10
        
        # Pass movie_index if provided
        recommendation = movie_recommendation(title, number, movie_index)

    return render(request, 'recommendation/movies.html', {
        'recommendation' : recommendation
    })

def autocomplete(request):
    """
    API endpoint for movie autocomplete suggestions
    """
    query = request.GET.get('q', '')
    suggestions = get_movie_suggestions(query, limit=50)
    return JsonResponse({'suggestions': suggestions})
