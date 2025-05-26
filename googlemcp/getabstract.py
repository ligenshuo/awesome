import requests
from bs4 import BeautifulSoup
import time
from scholarly import scholarly
import re
import random

user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
]
def get_random_user_agent():
    return random.choice(user_agents)

def getieeeabstract (url):
    match = re.search(r'document/(\d+)', url)
    if match:
        ieee_id = match.group(1)
        print(f"提取的 IEEE ID：{ieee_id}")
    else:
        print("❌ 未找到文献 ID")
    url = f'https://ieeexplore.ieee.org/rest/document/{ieee_id}/snippet'
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": f"https://ieeexplore.ieee.org/document/{ieee_id}/",
        "Origin": "https://ieeexplore.ieee.org"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 提取 <div> 内的纯文本
        text = soup.find('p').get_text(strip=True)
        print("✅ ieee摘要内容：\n", text)
        return text
    else:
        print(f"❌ 请求失败，状态码：{response.status_code}")


def getarxivabstract(url):
    # 发送 GET 请求
    headers = {
        "User-Agent": get_random_user_agent()
    }
    response = requests.get(url, headers=headers)

    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取摘要内容
    abstract_tag = soup.find('blockquote', class_='abstract')
    if abstract_tag:
        # 去掉 "Abstract:" 描述符，只保留正文
        descriptor = abstract_tag.find('span', class_='descriptor')
        if descriptor:
            descriptor.extract()  # 删除“Abstract:”部分
        abstract_text = abstract_tag.get_text(strip=True)
        print("✅ arxiv摘要内容：", abstract_text)
        return abstract_text
    else:
        print("未找到摘要。")

def Data_cleaning(text):
    # 匹配形如 [数字]，并删除
    cleaned_text = re.sub(r'\[\d+\]', '', text)
    # 去除多余空格
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text
def getabstract(url):
    print(url)
    abstract = ""
    if "ieeexplore.ieee.org" in url:
        # 抓取 IEEE 摘要
        abstract = getieeeabstract(url)   # 注意函数名拼写
    elif "arxiv.org" in url:
        abstract = getarxivabstract(url)
    return Data_cleaning(abstract)
