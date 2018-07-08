from movies import simple_get
from bs4 import BeautifulSoup
import operator
import os
import urllib.request

def get_movies():
    url = 'https://www.imdb.com/list/ls055592025/'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response,'html.parser') # parse response as html
        movies = []
        for h in html.find_all('h3'):
            if h.find('a') is not None and len(h.find('a').text) > 2: # problem, the last movie takes as doble end of line
                movies.append(h.find('a').text)

        for x in range(0,len(movies)):
            print('{}. {}'.format(x+1, movies[x]))

        return list(movies)


def top5_oscar(): # get top 5 rewarded by oscar movies
    url = 'https://www.imdb.com/list/ls055592025/'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        movies = []

        for h in html.find_all('div', {'class' :'lister-item'}): # go to <div class = lister-item> each class contains info about movie
            name = h.find('h3').find('a').text #get name of movie
            for p in h.find_all('div', {'class' :'list-description'}):
                rewards = p.find('p').text # get string with oscars (contains many info as a string, we're looking only for oscar)
            pos = rewards.find('Oscars: ')
            oscar = ""
            while True:
                if rewards[pos+8].isdigit():
                    oscar = oscar + rewards[pos+8]
                    pos = pos + 1
                else:
                    break

            #print('{} : {}'.format(name,oscar))
            movies.append((name,int(oscar)))
            movies.sort(key=operator.itemgetter(1),reverse = True)

    print(movies[:5])

def get_pictures():
    url = 'https://www.imdb.com/list/ls055592025/'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        pictures = []
        mkdir = os.makedirs('posters')
        count = 1
    for i in html.find_all('div', {'class' :'lister-item'}):
        pic = i.find('img') # link to a pic
        name = pic['alt'] # name of file
        dir = os.path.join('posters',str(count)+ '. ' + name + '.jpg')
        urllib.request.urlretrieve(pic['loadlate'], dir)
        count = count+1
        #print(pic['loadlate'])

get_pictures()
