from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
import re

def index(request):
    url = request.GET.get('url', '')

    source = requests.get(url).text

    result = {
        'title': '',
        'ingredients': []
    }

    soup = BeautifulSoup(source, features="html.parser")

    for a in soup.findAll('div', attrs={'class': 'recipe--ingredients-html-item col-md-8'}):
        ingredients = a.findAll('li')
        for i in ingredients:
            x = re.findall("[0-9]+", i.text)
            y = re.findall("[a-zA-ZÀ-ú]{3,}", i.text)
            result['ingredients'].append({ "value": x, "label": y })
    for x in soup.find('div', attrs={'class': 'recipe--header'}):
        if (x.find('h1') != -1):
            result['title'] = x.find('h1').text
    return JsonResponse(result, safe=False)