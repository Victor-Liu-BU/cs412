# file: restaurant/views.py
# Author: Ting Shing Liu, 9/16/25
# Description: views files that contains all of the functions for the restaurant app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import time
import random
from datetime import datetime, timedelta

# A dictionary to contain the special menu
special = {
    "item":["Pork Belly Bun", "Fried Chicken Bun", "Sukiyaki Beef Bun"],
    "price": "$4.5"
}

def main(request):
    """Respond to the URL 'main', delegate work to a template.
    Contains context for images to be passed into the template"""

    template_name = "restaurant/main.html"

    context = {
        "time": time.ctime(), # Uses the time module for the footer
        'image': ["https://static.wixstatic.com/media/b1cbcf_fe7df4994d0d43609eefd6976889f405~mv2.jpg/v1/fill/w_376,h_124,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/meallogo.jpg",
                "https://static.wixstatic.com/media/b1cbcf_43388bef76b5434c888db28dcdcb8d02~mv2.jpg/v1/fill/w_640,h_876,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b1cbcf_43388bef76b5434c888db28dcdcb8d02~mv2.jpg"]
    }
    
    return render(request, template_name, context=context)

def order(request):
    """Respond to the URL 'order', contains context"""

    template_name = "restaurant/order.html"

    context = {
        "time": time.ctime(), # For the footer
        "special": special["item"][random.randint(0,2)], # Display a random special item 
        "price": special["price"] # Price is fixed for the special item
    }

    return render(request, template_name, context=context)

def confirmation(request):
    """Process the form submission and generate a response"""

    template_name = "restaurant/confirmation.html"

    # A dictionary with all of the menu items as key and its price as value
    prices = {
        "isshindo_ramen": 16.0,
        "curry": 5.5,
        "beef_sukiyaki": 5.5,
        "chicken_katsu": 5.5,
        "extra_ramen": 2.0,
        "extra_egg": 1.0,
        "extra_pork": 2.0,
        "special": 4.5,
    }
    # check if POST data was sent with the HTTP POST message:
    if request.POST:
        # Make a dictionary ordered to keep track of the items that were selected during the ordering page
        ordered = {}
        total_price = 0.0

        # Loop through the items from the form submission
        for item_name in request.POST:
            # Check if the submitted item is in our price list
            if item_name in prices:
                # Append to our ordered dictionary with the item name as key and "Ordered" as value
                full_item_name = request.POST.get(item_name)
                ordered[full_item_name] = "Ordered"
                
                # Add the price from our dictionary
                total_price += prices[item_name]
        
        # Calculate the ready-by time by taking the current time and using timedelta to specify the minutes to add in time format
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))
        formatted_ready_time = ready_time.strftime("%I:%M %p") # %I for the hour, %M for the minute, and %p for PM/AM

        context = {
            "ordered_items": ordered,
            "name": request.POST.get("name") or "Guest", # The checkbox could be blank so provide a default value in such cases
            "phone_number": request.POST.get("phone_number") or "Not provided",
            "email": request.POST.get("email") or "Not provided",
            "time": time.ctime(),
            "total_price": f"{total_price:.2f}", # Format price
            "ready_by_time": formatted_ready_time,
        }

        return render(request, template_name, context=context)