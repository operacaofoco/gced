#%%
import requests
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from multiprocessing import Pool
#%%

url = 'http://172.16.1.115/'

options = Options()
#options.headless = True
profile = webdriver.FirefoxProfile()
profile.set_preference('permissions.default.image', 2)
options.profile = profile
driver = webdriver.Firefox(options=options)
# %%
driver.get(url)
# %%
soup = driver.find_element(By.CLASS_NAME, 'pagination')
pages = int(soup.text.split('\n')[-2])
pages
# %%
#options = Options()
#options.headless = True
#driver = webdriver.Firefox(options=options)
def scrape_page(page):
    print('inicio',page)
    driver.get(f'http://172.16.1.115/videos/find?is_routine=on&dt_start=2022-01-01T00%3A00&dt_end=2023-12-31T00%3A00&page={page}')
    df = pd.read_html(driver.page_source)
    df2 = [linha.T for linha in df]
    v = driver.find_elements(By.CLASS_NAME, 'video-play-button')
    b2 = [b.get_attribute('data-video-id') for b in v]
    print(len(b2))
    for i in range(len(b2)):
        df2[i]['id'] = b2[i]
    df3 = pd.concat(df2[:-1], axis=0)
    paginas.append(df3)
    print('fim',page, len(paginas))
# %%
# num_workers = 5
# pool = Pool(processes=num_workers)
# pool.map(scrape_page, range(1, 11))
# pool.close()
# pool.join()
paginas = []
#%%
for i in range(1,1000):
    scrape_page(i)

# %%
df_total = pd.concat(paginas)
df_total.drop_duplicates('id', inplace=True)
df_total
# %%
df_total.to_excel('data/log_camera5.xlsx')
# %%
