from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def show_form(request):
    """Show the form to the user"""

    template_name = "formdata/form.html"

    return render(request, template_name)

def submit(request):
    """Process the form submission and generate a response"""

    template_name = "formdata/confirmation.html"
    print(request)

    # check if POST data was sent with the HTTP POST message:
    if request.POST:

        # extract form fields into variables:
        name = request.POST["name"]
        favorite_color = request.POST["favorite_color"]

        # create context for use in the variable

        context = {
            'name': name,
            'favorite_color': favorite_color
        }

    return render(request, template_name=template_name, context=context)