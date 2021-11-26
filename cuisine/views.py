from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
import re

def index(request):
    url = request.GET.get('url', '')

    source = requests.get(url, verify=False).text

    result = {
        'title': '',
        'ingredients': []
    }

    soup = BeautifulSoup(source, features="html.parser")

    for a in soup.findAll('div', attrs={'class': 'recipe-detail-live-ingredient'}):
        ingredients = a.findAll('v-list-item__title:not(.primary--text)')
        for i in ingredients:
            x = re.findall("[0-9]+", i.text)
            y = re.findall("[a-zA-ZÀ-ú]{3,}", i.text)
            result['ingredients'].append({ "value": x, "label": y, 'raw': i.text })
    for x in soup.find('span', attrs={'class': 'recipe-title'}):
        result['title'] = x.find('h1').text
    return JsonResponse(result, safe=False)
