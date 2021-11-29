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

    ajaxUrl = "https://fr.monsieur-cuisine.com/wp-admin/admin-ajax.php"

    body = soup.find('body')
    bodyClassList = body['class']
    recipeId = ""

    for className in bodyClassList:
        if re.search("postid", className):
            recipeId = className.replace("postid-", "")

    res = requests.post(ajaxUrl, data={"action": "load_recipe_post", "recipe_id": recipeId}, verify=False).json()
    for ingredient in res['recipe']['serving_sizes'][0]['ingredients']:
        x = re.findall("[0-9]+", ingredient['name'])
        y = re.findall("[a-zA-ZÀ-ú]{3,}", ingredient['name'])
        result['ingredients'].append({ "value": x, "label": y, 'raw': ingredient['name'] })

    result['title'] = res['recipe']['title']
