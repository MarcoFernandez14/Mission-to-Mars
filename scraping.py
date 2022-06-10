
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


# Function to re-use the code.
def scrape_all():
    # Initiate headless driver for deployment
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) # Headless=False allows to see the scraping

    # This line of code tells Python that we'll be using our mars_news function to pull this data.
    news_title, news_paragraph = mars_news(browser)
    img_url_titles = mars_hemis(browser)

    # Run all scraping functions and store results in dictionary.
    # It runs all of the functions we've created and it also stores all of the results.
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": img_url_titles,
      "last_modified": dt.datetime.now()
    }


    # Stop webdriver and return data
    browser.quit()
    
    return data


# Function to re-use the code. Use "browser" variable.
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # news_title
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        # news_p

    except AttributeError:
        return None, None


    return news_title, news_p


# ### Featured Images

# Function to re-use the code. Use "browser" variable.
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # img_url

    return img_url


# Function to re-use the code
def mars_facts():

    # Add try/except for error handling. Use BaseException as 'read_html' is a Pandas function which can have other errors than AttributeErrors
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    # df

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


# Function to re-use the code
def mars_hemis(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):

        # Browse through each article
        browser.find_by_css('a.product-item h3')[i].click()

        # Parse the resulting html with soup
        html = browser.html
        hemisphere_soup = soup(html, 'html.parser')
    
        # Scrape
        img_url = hemisphere_soup.find('li').a.get('href')
        # image_url
        title = hemisphere_soup.find('h2', class_='title').text
        # title
    
        # Store into a dictionary
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)

        # Browse back to repeat
        browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls



# Flask connection
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
