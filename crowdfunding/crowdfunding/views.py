from django.http import JsonResponse

def custom_404_view(request, exception):
    return JsonResponse({'error': 'The resource was not found.'}, status=404)

def custom_500_view(request):
    return JsonResponse({'error': 'An internal server error occurred.'}, status=500)
