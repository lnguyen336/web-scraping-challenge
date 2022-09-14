# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time
from IPython.display import display
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # Note: Replace the executable path with your actual path to the chrome driver
    executable_path = {'executable_path': 'C:/Users/User/.wdm/drivers/chromedriver/win32/103.0.5060/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless = False)

def scrape():
    browser = init_browser()

    # Create mars_data dictionary to insert for mongo
    mars_data = {}
    print('Starting Scraper')

    #############################################################

    # Visit Mars News Site URL using splinter
    NASA_url = 'https://redplanetscience.com/'
    browser.visit(NASA_url)

    # One second time delay for error purposes
    time.sleep(1)

    # Convert the browser html to a soup object
    html = browser.html
    NASA_soup = soup(html, 'html.parser')

    # Extract Title Text
    title = NASA_soup.find_all('div', class_ = 'content_title')[0].text

    # Extract Paragraph Text
    paragraph = NASA_soup.find_all('div', class_ = 'article_teaser_body')[0].text

    ##############################################################

    # Visit Mars Space Images URL using splinter
    Mars_image_url = 'https://spaceimages-mars.com/'
    browser.visit(Mars_image_url)

    # One second time delay for error purposes
    time.sleep(1)

    # Convert the browser html to a soup object
    html = browser.html
    image_soup = soup(html, 'html.parser')

    # Extract the current Featured Mars Image
    results = image_soup.find_all('a', class_ = 'fancybox-thumbs')
    image_urls = []
    for result in results:
        image_urls.append(Mars_image_url + result['href'])

    # Assign the URL string to a variable called featured_image_url
    featured_image_url = Mars_image_url + results[0]['href']

    ###############################################################

    # Visit Mars Facts Webpage URL using splinter
    Mars_fact_url = 'https://galaxyfacts-mars.com/'

    # Use Pandas' function 'read_html' to parse the URL and scrape all data
    tables = pd.read_html(Mars_fact_url)

    # Convert tabular data into a dataframe to rename columns
    facts_table = tables[0]

    # Rename columns and reset index
    facts_table = facts_table.rename(columns = {0: 'Description', 1: 'Mars', 2: 'Earth'})
    facts_table.set_index('Description', inplace = True)

    # Use Pandas to convert dataframe to HTML table string
    mars_html = facts_table.to_html()

    ##############################################################

    # Visit Astrogeology Webpage URL using splinter
    Astrogeology_url = 'https://marshemispheres.com/'
    browser.visit(Astrogeology_url)

    # One second time delay for error purposes
    time.sleep(1)

    # Convert the browser html to a soup object
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    # Extract the collect title and image URLs for high-resolution images for each hemisphere
    results = hemi_soup.find_all('div', class_ = 'item')
    hemi_urls = []
    for result in results:
        title = result.find('h3').get_text()
        img_url = result.find('img', class_ = 'thumb')['src']
        img_url = Astrogeology_url + img_url
        hemi_urls.append({'title': title, 'img_url': img_url})

    ############################################################

    # Save all the above data in the empty dictionary
    mars_data = {'title': title,
    'paragraph': paragraph,
    'featured_image': featured_image_url,
    'facts_table': mars_html,
    'hemisphere_images': hemi_urls
    }

    ############################################################

    # Quit the browser
    browser.quit()
    return mars_data