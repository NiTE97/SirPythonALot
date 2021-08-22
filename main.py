import logging, sys, requests, re
import urllib.request as urllib
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

def scrapingThumbnails(list):
    i = 0
    max = len(list)
    links = [''] * max

    while i<max:

        links[i] = list[i].get('data-thumb_url')
        i+=1    
    
    links = links[4:]  

    return links

def scrapingNames(list):
    i = 0
    max = len(list)
    names = [''] * max

    while i<max:
        names[i] = list[i].get('title')
        i+=1    
    names = names[4:]
    
    return names

def scrapingLinksAndNames(list):
    i = 0
    max = len(list)
    links = [''] * max
    names = [''] * max

    while i<max:
        links[i] = "pornhub.com" + list[i].get('href')
        names[i] = list[i].get('title')

        i+=1  

    links = links[4:]  
    names = names[4:]

    return links, names

def scraping(keyword):
    pornhub = "https://pornhub.com/video/search?search="
    pornhub_suffix = "&page="
    youporn = "https://www.youporn.com/search/?search-btn=&query="

    #Search
    results = requests.get(pornhub + keyword + pornhub_suffix + "1")
    soup = BeautifulSoup(results.text, 'html.parser')
    list = soup.find_all(class_='rotating')
    list2 = soup.find_all(class_='fade')

    resultsLinks, resultsNames = scrapingLinksAndNames(list2)
    #resultsNames = scrapingNames(list2)
    resultsThumbnails = scrapingThumbnails(list)

    for i in range(2, 5):
        results2 = requests.get(pornhub + keyword + pornhub_suffix + str(i))
        soup2 = BeautifulSoup(results2.text, 'html.parser')
        list3 = soup2.find_all(class_='rotating')
        list4 = soup2.find_all(class_='fade')
        resultsLinksi, resultsNamesi = scrapingLinksAndNames(list4)
        resultsLinks = resultsLinks + resultsLinksi
        resultsNames = resultsNames + resultsNamesi
        #resultsNames = resultsNames + scrapingNames(list4)
        resultsThumbnails = resultsThumbnails + scrapingThumbnails(list3)    

    return resultsLinks, resultsNames, resultsThumbnails


@app.route("/results", methods=['POST','GET'])
def results():
    if request.method == 'GET':
        return home()
    if request.method == 'POST':
        form_data = request.form
        keyword = form_data["textinput"]
        resultsLinks, resultsNames, resultsThumbnails = scraping(keyword)
        lenght = len(resultsThumbnails)

        pornhub = "https://pornhub.com/video/search?search="
        pornhub_suffix = "&page="
        string = pornhub + keyword + pornhub_suffix + "2"
        return render_template('results.html',form_data = form_data, resultsThumbnails = resultsThumbnails, resultsNames = resultsNames
                                , resultsLinks = resultsLinks, lenght = lenght, string = string)

if __name__ =='__main__':
    app.run(debug=True)