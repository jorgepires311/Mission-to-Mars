from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from IPython.core.display import display, HTML
import pymongo

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    ## Set up Mongo DB connection
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define the 'dbMars' database in Mongo
    db = client.dbMars

    marsData = {}

    ##NASA Mars News
    urlMarsNews = 'https://mars.nasa.gov/news/'
    responseMarsNews = requests.get(urlMarsNews)
    soupMarsNews = BeautifulSoup(responseMarsNews.text, 'html.parser')
    # print(soupMarsNews.prettify())
    resultsMarsNews = soupMarsNews.find_all('div', class_="slide")
    # Loop through returned results
    for result in resultsMarsNews:
        # Error handling
        try:
            # Identify and return title of listing
            news_title = result.find('div', class_="content_title").text
            news_p = result.find('div', class_="rollover_description_inner").text
            # Print results only if title, price, and link are available
            if (news_title):
                marsData['news_title'] = news_title
                marsData['news_p'] = news_p
                exit
        except AttributeError as e:
            print(e)

    ##JPL Mars Space Images - Featured Image
    urlBaseMarsFeatureImg = 'https://www.jpl.nasa.gov'
    urlMarsFeatureImg = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = init_browser()
    browser.visit(urlMarsFeatureImg)
    html = browser.html
    soupMarsSplinter = BeautifulSoup(html, 'html.parser')
    imgContMarsSplinter = soupMarsSplinter.find('article', class_='carousel_item')
    marsData['featured_image_url'] = urlBaseMarsFeatureImg + imgContMarsSplinter.a['data-fancybox-href']

    ## Mars Weather
    urlMarsTwitter = "https://twitter.com/marswxreport?lang=en"
    responseMarsTwitter = requests.get(urlMarsTwitter)
    soupMarsTwitter = BeautifulSoup(responseMarsTwitter.text, 'html.parser')
    resultsMarsTwitter = soupMarsTwitter.find_all('li', class_="stream-item")
    resultsMarsTwitter
    for result in resultsMarsTwitter:
        try:
            if ('InSight' in result.find('p', class_="tweet-text").text):
                marsData['mars_weather'] = result.find('p', class_="tweet-text").text
                exit
        except AttributeError as e:
            print(e)

    ## Mars Facts
    urlFacts = "https://space-facts.com/mars/"
    dfFactsTables = pd.read_html(urlFacts)
    dfFactsTables = dfFactsTables[0]
    dfFactsTables.columns = ['Fact','Value']
    htmlFactsTables = dfFactsTables.to_html()
    marsData['mars_facts'] = htmlFactsTables


    ## Mars Hemispheres
    browser = init_browser()
    urlHemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(urlHemi)
    htmlHemi = browser.html
    soupHemi = BeautifulSoup(htmlHemi,'html.parser')
    listHemi = soupHemi.find_all('div',class_="item")
    urlsHemi = []
    for result in listHemi:
        try:
            urlsHemi.append('https://astrogeology.usgs.gov'+result.a['href'])
        except AttributeError as e:
            print(e)
    urlsHemi
    listDictHemi = []
    for url in urlsHemi:
        browser.visit(url)
        urlHTML = browser.html
        soupHTML = BeautifulSoup(urlHTML,'html.parser')
        urlTitle = soupHTML.find('h2',class_='title').text
        urlImg = 'https://astrogeology.usgs.gov'+soupHTML.find('img',class_='wide-image')['src']
        listDictHemi.append({'title':urlTitle,'img_url':urlImg})
    marsData['hemi'] = listDictHemi

    return marsData
