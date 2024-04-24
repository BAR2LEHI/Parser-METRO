import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept': '*/*'
}

METRO_URL = 'https://online.metro-cc.ru'
CATEGORY = 'Рыба, икра, морепродукты'
SUBCATEGORY = 'Живая и свежая рыба'


def get_source_category_html(driver, url, category, subcategory):
    try:
        driver.switch_to.new_window('tab')
        driver.get(url)
        time.sleep(7)
        driver.find_element(By.CSS_SELECTOR, '.header-button-catalog').click()
        driver.find_element(By.LINK_TEXT, category).click()
        driver.find_element(By.LINK_TEXT, subcategory).click()
        time.sleep(5)
        return driver.page_source
    
    except Exception as ex:
        print(ex)
    
    finally:
        driver.close()
        main_page = driver.window_handles[0]  
        driver.switch_to.window(main_page)


def get_products_urls(page_source):
    soup = BeautifulSoup(page_source, 'lxml')
    products_div = soup.find_all('div', class_='catalog-2-level-product-card')

    products_urls = []
    for product_url in products_div:
        product_url = product_url.find('div', 'product-card-photo__content').find('a').get('href')
        products_urls.append(product_url)
    
    return products_urls


def get_products_data(driver, main_url, products_urls):

    for url in products_urls:
        try:
            product_full_url = main_url + url
            driver.switch_to.new_window('tab')
            driver.get(product_full_url)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            try:
                product_article = soup.find(
                    'p', {'itemprop': 'productID'}
                ).text.split(':')[-1].strip()
            except Exception as ex:
                product_article = None
        
            try:
                product_name = soup.find(
                    'h1', class_='product-page-content__product-name'
                ).find('span').text.strip()
            except Exception as ex:
                product_name = None

            try:
                li_elements = soup.find('div', class_='product-attributes').find_all('li')
                brand = None
                for li in li_elements:
                    span_tag_brand = li.find('span').text.strip()
                    if span_tag_brand == 'Бренд':
                        brand = li.find('a').text.strip()
                        break
            except Exception as ex:
                brand = None

            try:
                div_prices = soup.find(
                    'div', class_='product-unit-prices__actual-wrapper'
                )
                rubles_price_elem = div_prices.find(
                    'span', class_='product-price__sum-rubles'
                )
                penny_price_elem = div_prices.find(
                    'span', class_='product-price__sum-penny'
                )
                
                if penny_price_elem is not None:
                    actual_price = ''.join((rubles_price_elem.text + penny_price_elem.text).split('\xa0'))
                else:
                    actual_price = ''.join(rubles_price_elem.text.split('\xa0'))
            except Exception as ex:
                actual_price = None

            try:
                div_old_price = soup.find(
                    'div', class_='product-unit-prices__old-wrapper'
                )
                old_rubles_price_elem = div_old_price.find(
                    'span', class_='product-price__sum-rubles'
                )
                old_penny_price_elem = div_old_price.find(
                    'span', class_='product-price__sum-penny'
                )
                if old_penny_price_elem is not None:
                    old_price = ''.join((old_rubles_price_elem.text + old_penny_price_elem.text).split('\xa0'))
                else:
                    old_price = ''.join(old_rubles_price_elem.text.split('\xa0'))
                
            except Exception as ex:
                old_price = None
                
            product = {
                'id': product_article,
                'name': product_name,
                'brand': brand,
                'actual_price': actual_price,
                'old_price': old_price
            }
            print(product)

        finally:
            driver.close()
            main_page = driver.window_handles[0]  
            driver.switch_to.window(main_page)


def main(driver):
    page_source = get_source_category_html(
        driver=driver,
        url=METRO_URL, 
        category=CATEGORY, 
        subcategory=SUBCATEGORY
    )
    products_urls = get_products_urls(page_source)
    get_products_data(
        main_url=METRO_URL,
        products_urls=products_urls,
        driver=driver
    )


if __name__ == '__main__':
    try:
        driver = webdriver.Firefox(
                            service=Service(GeckoDriverManager().install())
                        )
        driver.maximize_window()
        main(driver)
    finally:
        driver.quit()
