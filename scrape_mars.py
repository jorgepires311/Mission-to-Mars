from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from IPython.core.display import display, HTML


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def marsNews():
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
                print('******************')
                print(news_title + news_p)
        except AttributeError as e:
            print(e)

def marsImages():
    browser = init_browser()
    browser.visit(urlMarsFeatureImg)
    html = browser.html
    soupMarsSplinter = BeautifulSoup(html, 'html.parser')
    imgContMarsSplinter = soupMarsSplinter.find('article', class_='carousel_item')
    featured_image_url = urlBaseMarsFeatureImg + imgContMarsSplinter.a['data-fancybox-href']
    print('splinter method: ' + featured_image_url)
    browser.visit(featured_image_url)

def marsWeather():
    urlMarsTwitter = "https://twitter.com/marswxreport?lang=en"
    responseMarsTwitter = requests.get(urlMarsTwitter)
    soupMarsTwitter = BeautifulSoup(responseMarsTwitter.text, 'html.parser')
    resultsMarsTwitter = soupMarsTwitter.find_all('li', class_="stream-item")
    resultsMarsTwitter
    for result in resultsMarsTwitter:
        try:
            if ('InSight' in result.find('p', class_="tweet-text").text):
                mars_weather = result.find('p', class_="tweet-text").text
                exit
        except AttributeError as e:
            print(e)
            
    print('Latest weather on Mars: ' + mars_weather)

def marsFacts():
    urlFacts = "https://space-facts.com/mars/"
    dfFactsTables = pd.read_html(urlFacts)
    dfFactsTables = dfFactsTables[0]
    dfFactsTables.columns = ['Fact','Value']
    htmlFactsTables = dfFactsTables.to_html()
    print(htmlFactsTables)

def marsHemisphere():
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
        
    listDictHemi