from django.shortcuts import render
from django.http import JsonResponse
from .similarity import movie_recommendation, get_movie_suggestions

# Create your views here.
def index(request):
    recommendation = []
    # Check for title in GET or POST
    title = request.GET.get('title') or request.POST.get('title')
    
    if title:
        number = request.GET.get('number') or request.POST.get('number')
        # Default to 10 if number is missing/invalid, though HTML enforces it.
        # It's safer to handle conversion errors
        try:
            number = int(number)
        except (ValueError, TypeError):
            number = 10
            
        recommendation = movie_recommendation(title, number)

    return render(request, 'recommendation/movies.html', {
        'recommendation' : recommendation
    })

def autocomplete(request):
    """
    API endpoint for movie autocomplete suggestions
    """
    query = request.GET.get('q', '')
    suggestions = get_movie_suggestions(query, limit=10)
    return JsonResponse({'suggestions': suggestions})
