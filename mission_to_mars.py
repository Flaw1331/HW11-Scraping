
# coding: utf-8

#Import Dependencies
import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from sys import platform


def scrape():

    # Initialize Things
    def init_browser():
        if platform == "darwin":
            executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        else:
            executable_path = {'executable_path': 'chromedriver.exe'}
        return Browser("chrome", **executable_path, headless=False)


    # Defining URLs to use
    nasa_url = 'https://mars.nasa.gov/news/'
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    twit_url = 'https://twitter.com/marswxreport?lang=en'
    facts_url = 'https://space-facts.com/mars/'
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # Simply soup call for urls
    def getResponse(url):
        return BeautifulSoup(requests.get(url).text, 'html.parser')


    # Pull title and desc from NASA website
    nasa_soup = getResponse(nasa_url)
    title = nasa_soup.find('div', class_='content_title').get_text().strip('\n')
    desc = nasa_soup.find('div', class_='rollover_description_inner').get_text().strip('\n')


    # Image rip
    img_soup = getResponse(img_url)
    picture = img_soup.find(class_='carousel_item')['style'].lstrip('''background-image: url(''').rstrip(');')
    fin_img_url = 'https://www.jpl.nasa.gov' + picture.strip("'")


    # Twitter rip for weather
    twit_soup = getResponse(twit_url)
    result = twit_soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = result.get_text()


    # Pulling Table data
    facts_df = pd.DataFrame(pd.read_html(facts_url)[0])
    facts_df.columns = ['Category','Measurement']
    facts_df.set_index('Category', inplace=True)
    table_string = facts_df.to_html()

    # Hemisphere imgs
    astro_soup = getResponse(astro_url)
    hemisphere_image_urls = []

    # Links
    links = ['https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
            'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
            'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
            'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg']

    # Looping through each item and appening to list
    for x in range(0, len(astro_soup.findAll(class_="item"))):
        img_link = {astro_soup.findAll(class_="item")[x].find('a').find('div').get_text(): links[x]}
        hemisphere_image_urls.append(img_link)


    # Creating dict
    mars_dict = {
        'news_title' : title,
        'news_summary' : desc, 
        'featured_image_url' : fin_img_url,
        'mars_weather' : mars_weather,
        'table_string' : table_string,
        'hemisphere_image_urls' : hemisphere_image_urls}

    # Setting up return
    return mars_dict

