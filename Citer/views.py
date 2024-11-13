from django.shortcuts import render
from django.http import JsonResponse
from _AutoCitation.main import AutoCitation
from django.views.decorators.http import require_GET
import time
import os

@require_GET
def check_log_step(request):
    step = request.GET.get('step')
    log_file_path = './_AutoCitation/log/process.log'
    if not step:
        return JsonResponse({'error': 'No step specified'}, status=400)
    try:
        with open(log_file_path, 'r') as log_file:
            # Check if the log contains the step as a substring
            log_content = log_file.read()
            step_found = step in log_content
            return JsonResponse({'step_found': step_found})
    except FileNotFoundError:
        return JsonResponse({'error': 'Log file not found'}, status=404)

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
            # Update the log file with the steps
            log_file_path = './_AutoCitation/log/process.log'
            with open(log_file_path, 'a') as log_file:
                log_file.write('Reading and filtering text\n')
                log_file.write('Classifying type of text\n')
                log_file.write('Generating queries\n')
                log_file.write('Getting links\n')
                log_file.write('Getting citations\n')
                log_file.write('Final result\n')
            return JsonResponse({"success": True, "message": "Processing completed successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method."})

def show_results(request):
    # Add any logic here to prepare data for the results page
    return render(request, 'results.html')