# # Step 1 - Scraping 

# ## Dependencies

import pymongo
import requests
import time
import pandas as pd
from flask import Flask, render_template, redirect
from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # When I was trying to call the chromedriver I had an issue. Calling the hole directory was the only thing that solved the issue. 
    executable_path = {"executable_path": "C:\\Users\\Luis Alejandro\\Desktop\\Tareas y Clase\\12 Web_Scraping\\Missions_to_Mars\\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # ## NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[16].text
    news_p = soup.find_all('div', class_='article_teaser_body')[16].text


    # ## JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_url = soup.find('article')['style'].replace("background-image: url('",'').replace("');", '')
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url


    # ## Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweets = soup.find_all('article', role="article")
    mars_weather = tweets[0].find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    mars_weather = str(mars_weather[4].text)


    # ## Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_df = pd.read_html(html)[0]
    mars_df.columns = ['Mars Profile', 'Value']
    mars_facts = mars_df.to_html(index=False)


    # ## Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    products = soup.find_all('div', class_='item')
    hemisphere_image_urls = []

    for image in products: 
        title = image.find('h3').text
        image_url = image.find('a', class_='itemLink product-item')['href']
        
        url = 'https://astrogeology.usgs.gov' + image_url
        browser.visit(url)
        image_url = browser.html 
        soup = BeautifulSoup(image_url, 'html.parser')
        
        image_url = soup.find('img', class_='wide-image')['src']
        full_image = 'https://astrogeology.usgs.gov' + image_url
    
        hemisphere_image_urls.append({"title" : title, "img_url" : full_image})

    # Dictionary
    dictionary = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return dictionary