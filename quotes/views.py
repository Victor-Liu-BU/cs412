# file: quotes/views.py

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
def quote(request):
    template_name = 'quotes/quote.html'

    quote_list = ["“You are in danger of living a life so comfortable and soft, that you will die without ever realizing your true potential.”",
                  "“It won’t always go your way, so you can’t get trapped in this idea that just because you’ve imagined a possibility for yourself that you somehow deserve it. Your entitled mind is dead weight. Cut it loose. Don’t focus on what you think you deserve. Take aim on what you are willing to earn!”",
                  "“No one is going to come help you. No one's coming to save you.”"]
    image_list = ["https://img.nmcdn.io/e1/w:570,h:590,v:1/iava/wp-content/uploads/2024/09/David_Goggins-e1725986720286.jpg?s=b0ecf840",
                  "https://www.airofin.com/cdn/shop/articles/goggins.jpg?v=1600810012",
                  "https://miro.medium.com/v2/resize:fit:1100/format:webp/1*uN6QR16cg29rJcJy38JClg.jpeg"]
    context = {
        "quote": quote_list[random.randint(0,2)],
        "image": image_list[random.randint(0,2)]
    }

    return render(request, template_name, context)

def show_all(request):
    template_name = 'quotes/show_all.html'

    context = {
        "quote": ["“You are in danger of living a life so comfortable and soft, that you will die without ever realizing your true potential.”",
                  "“It won’t always go your way, so you can’t get trapped in this idea that just because you’ve imagined a possibility for yourself that you somehow deserve it. Your entitled mind is dead weight. Cut it loose. Don’t focus on what you think you deserve. Take aim on what you are willing to earn!”",
                  "“No one is going to come help you. No one's coming to save you.”"],
        "image": ["https://img.nmcdn.io/e1/w:570,h:590,v:1/iava/wp-content/uploads/2024/09/David_Goggins-e1725986720286.jpg?s=b0ecf840",
                  "https://www.airofin.com/cdn/shop/articles/goggins.jpg?v=1600810012",
                  "https://miro.medium.com/v2/resize:fit:1100/format:webp/1*uN6QR16cg29rJcJy38JClg.jpeg"]
    }

    return render(request, template_name, context)

def about(request):
    '''Respond to the URL 'about', delegate work to a template'''

    template_name = 'quotes/about.html'
    return render(request, template_name)