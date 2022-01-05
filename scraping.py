# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_all():
    data = {}
    data = mars_facts()
    return data

def mars_facts():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup_img = BeautifulSoup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # 4. Use the DevTools to inspect the page for the proper elements to scrape. You will need to retrieve the full-resolution image for each of Mars's hemispheres.
    # 5. In Step 2, create a list to hold the .jpg image URL string and title for each hemisphere image.
    title_raw_soup = soup_img.find_all('h3')
    hemisphere_title = []
    for title in title_raw_soup:
        hemisphere_title.append(title.text)
    # for debug purpose from Jupyter Notebook
    for title in hemisphere_title:
        print(title)
    
    # Step#1
    # get all img entries
    rel_image_lst = soup_img.find_all('img')

    # Step#2 
    # loop through to find matching title and save that img only 
    # concatinate with orginal url and print show!!
    idx = 0
    for img_raw in rel_image_lst:
        if re.search(hemisphere_title[idx],img_raw['alt']):
            img_url = url + img_raw['src']
            hemisphere = {}
            hemisphere['img_url'] = img_url
            hemisphere['title'] = hemisphere_title[idx]
            hemisphere_image_urls.append(hemisphere)  
            idx+=1
            if ( idx >= 4 ): 
                break
    for items in hemisphere_image_urls:
        print (items)
        
    browser.quit()

    return hemisphere_image_urls
