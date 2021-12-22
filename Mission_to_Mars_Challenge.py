# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import re

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
#news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
# news_p

# ### JPL Space Images Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

html = browser.html
img_soup = soup(html, 'html.parser')
# img_soup

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
# img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
# img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
# img_url


df = pd.read_html('https://galaxyfacts-mars.com')[0]
# df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
# df

df.to_html()

# ### Hemispheres
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

html = browser.html
soup_img = soup(html, 'html.parser')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# 4. Use the DevTools to inspect the page for the proper elements to scrape. You will need to retrieve the full-resolution image for each of Mars's hemispheres.
# 5. In Step 2, create a list to hold the .jpg image URL string and title for each hemisphere image.
title_raw_soup = soup_img.find_all('h3')
hemisphere_title = []
for title in title_raw_soup:
    hemisphere_title.append(title.text)

# for title in hemisphere_title:
#     print(title)
    

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
        dict_url_title = {}
        dict_url_title['img_url'] = img_url
        dict_url_title['title'] = hemisphere_title[idx]
        hemisphere_image_urls.append(dict_url_title)  
        idx+=1
        if ( idx >= 4 ): 
            break


# 4. Print the list that holds the dictionary of each image url and title.
# hemisphere_image_urls


# 5. Quit the browser
browser.quit()


# In[ ]:




