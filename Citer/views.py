from django.shortcuts import render
from django.http import JsonResponse
from _AutoCitation.main import AutoCitation

def home(request):
    """Renders the home template with the Run All button."""
    return render(request, 'home.html')

def run_all(request):
    """Handles the run_all request, executing AutoCitation's run_all method."""
    if request.method == "POST":
        # Get the text to classify from the POST request
        text_to_classify = request.POST.get('text_to_classify')

        # Initialize and run AutoCitation
        auto_citation = AutoCitation(text_to_classify)
        try:
            auto_citation.run_all()
            return JsonResponse({"success": True, "message": "Processing completed successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})
def show_results(request):
    # Add any logic here to prepare data for the results page
    return render(request, 'results.html')