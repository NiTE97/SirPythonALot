import logging, sys, requests, re
import urllib.request as urllib
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

app = Flask(__name__)

#Default route
@app.route("/")
@app.route("/index")
def home():
    return render_template('index.htmx')

#Function to scrape Pornhub 
#list = list for links and names
#list2 = list for thumbnails
def scrapingLinksAndNamesAndThumbnailsFromPornhub(list, list2):
    i = 0
    max = len(list)
    maxWithoutPremium = max - 4
    links, names, thumbnails = [''] * max, [''] * max, [''] * max

    while i<max:
        links[i] = "pornhub.com" + list[i].get('href')
        names[i] = list[i].get('title')
        thumbnails[i] = list2[i].get('data-thumb_url')

        i+=1  

    links = links[4:maxWithoutPremium]  
    names = names[4:maxWithoutPremium]
    thumbnails = thumbnails[4:maxWithoutPremium]

    return links, names, thumbnails

#Function to scrape Pornhub 
#list = list for names and thumbnails
#list2 = list for links
def scrapingLinksAndNamesAndThumbnailsFromYouporn(list, list2):
    i = 0
    max = len(list2)
    links, names, thumbnails = [''] * max, [''] * max, [''] * max

    while i<max:
        links[i] = "youporn.com" + list2[i].get('href')
        names[i] = list[i].get('alt')
        thumbnails[i] = list[i].get('data-thumbnail')

        i+=1  
    return links, names, thumbnails

def scraping(keyword, index):
    pornhub = "https://pornhub.com/video/search?search="
    suffix = "&page="
    youporn = "https://www.youporn.com/search/?query="
    #x = index * 1
    #y = index * 2
    
    #Temp Lists for loop
    resultsLinks, resultsNames, resultsThumbnails = [], [], []

    #Search Pornhub and Youporn
    #Development:
    for i in range(1, 2):
    #Deployment
    #for i in range(1, 5):
        #Scraping preparation Pornhub
        resultsPornhub = requests.get(pornhub + keyword + suffix + str(index))
        soupPornhub = BeautifulSoup(resultsPornhub.text, 'html.parser')
        #links and names
        listPornhub = soupPornhub.find_all(class_='rotating')
        #thumbnails
        list2Pornhub = soupPornhub.find_all(class_='fade')

        #Scraping preparation Youporn
        resultsYouporn = requests.get(youporn + keyword + suffix + str(index))
        soupYouporn = BeautifulSoup(resultsYouporn.text, 'html.parser')
        #names and thumbnails
        listYouporn = soupYouporn.find_all(class_='js-videoPreview')
        #links
        list2Youporn = soupYouporn.find_all(class_='video-box-image')

        #Fill lists with results from Pornhub
        resultsLinksi, resultsNamesi, resultsThumbnailsi = scrapingLinksAndNamesAndThumbnailsFromPornhub(list2Pornhub, listPornhub)
        resultsLinks = resultsLinks + resultsLinksi
        resultsNames = resultsNames + resultsNamesi
        resultsThumbnails = resultsThumbnails + resultsThumbnailsi  

        #Fill lists with results from Youporn
        resultsLinksp, resultsNamesp, resultsThumbnailsp = scrapingLinksAndNamesAndThumbnailsFromYouporn(listYouporn, list2Youporn)
        resultsLinks = resultsLinks + resultsLinksp
        resultsNames = resultsNames + resultsNamesp
        resultsThumbnails = resultsThumbnails + resultsThumbnailsp 

    return resultsLinks, resultsNames, resultsThumbnails


@app.route("/results", methods=['POST','GET'])
def results():
    #Check if form is POST
    if request.method == 'GET':
        return home()
    if request.method == 'POST':
        #Get input from form
        form_data = request.form
        global keyword 
        keyword = form_data["textinput"]
        #Scraping Web
        resultsLinks, resultsNames, resultsThumbnails = scraping(keyword, 1)
        global index 
        index = 2
        lenght = len(resultsThumbnails)
        #Display results
        return render_template('results.htmx',form_data = form_data, resultsThumbnails = resultsThumbnails, resultsNames = resultsNames
                                , resultsLinks = resultsLinks, lenght = lenght)

@app.route("/results/more")
def more():
    #Scraping Web
        global index
        resultsLinks, resultsNames, resultsThumbnails = scraping(keyword, index)
        lenght = len(resultsThumbnails)
        index += 1
        #Display results
        return render_template('more.htmx',keyword = keyword, resultsThumbnails = resultsThumbnails, resultsNames = resultsNames
                                , resultsLinks = resultsLinks, lenght = lenght, index = index)
    
if __name__ =='__main__':
    app.run(debug=True)