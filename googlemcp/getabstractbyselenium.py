from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import time
from scholarly import scholarly
import re
import random

# 设置 ChromeDriver 路径
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 启用无头模式
# chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
chrome_driver_path = r'C:\Users\li283\Desktop\Chrome125.0.6422.142AndChromedrive125.0.6422.141\chromedriver.exe'  # 修改为你的路径
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def Data_cleaning(text):
    # 匹配形如 [数字]，并删除
    cleaned_text = re.sub(r'\[\d+\]', '', text)
    # 去除多余空格
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text
def getabstractselenium(url):
    print(f"\n正在处理：{url}")
    driver.get(url)
    time.sleep(5)  # 等待页面和脚本加载

    try:
        if "ieeexplore.ieee.org" in url:
            # 抓取 IEEE 摘要
            abstract_div = driver.find_element(By.CSS_SELECTOR, 'div.abstract-text')
            print("摘要：", abstract_div.text.strip())
        elif "arxiv.org" in url:
            # 抓取 arXiv 摘要
            abstract_div = driver.find_element(By.CSS_SELECTOR, 'blockquote.abstract')
            abstract_text = abstract_div.text.replace('Abstract: ', '').strip()
            print("摘要：", abstract_text)
            return  Data_cleaning(abstract_text)
        else:
            print("不支持的网站")
    except Exception as e:
        print("未找到摘要内容:", e)
    driver.quit()


