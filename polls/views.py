from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson
import requests
from bs4 import BeautifulSoup
import csv

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")

    response = requests.get('https://comunicachihuahua.desarrollosenlanube.net')

    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all(class_='jeg_post')

    with open('posts.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        headers = ['Title', 'Link', 'Image', 'Excerpt']
        csv_writer.writerow(headers)

        for post in posts:
            title = post.find(class_='jeg_post_title').get_text().replace('\n', '')
            link = post.find('a')['href']
            image = post.find(class_='thumbnail-container').find('img')['src']
            # image = 'imagen'
            excerpt = post.find(class_='jeg_post_excerpt').find('p').get_text().replace('\n', '')
            csv_writer.writerow([title, link, image, excerpt])

    csv_path = 'posts.csv'
    json_path = 'posts.json'

    data = {}

    with open(csv_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for index, rows in enumerate(csv_reader):
                id = index
                data[id] = rows

    with open(json_path, 'w') as json_file:
            json_file.write(simplejson.dumps(data, indent = 4))

    return HttpResponse(simplejson.dumps(data), content_type="application/json")

