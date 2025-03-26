import requests
import json
import time
import random
import os
import re
import string
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # 需要安装: pip install fake-useragent

# 添加 selenium 相关导入
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 你的豆瓣 UID
DOUBAN_UID = "148921757"
MOVIE_JSON_PATH = "data/movies.json"  # 存放电影数据
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = [5, 10, 20]  # 重试延迟时间（秒）
PAGE_SIZE = 15  # 每页电影数量
USE_SELENIUM = True  # 是否使用Selenium

# 生成随机bid
def generate_random_bid():
    """生成随机的豆瓣bid"""
    # bid格式为11位字母数字组合
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(11))

# 预生成一批随机bid
RANDOM_BIDS = [generate_random_bid() for _ in range(50)]

def get_random_cookie():
    """获取带有随机bid的Cookie"""
    bid = random.choice(RANDOM_BIDS)
    return f'bid={bid}'

def get_first_movie_id():
    """获取已有数据中的第一部电影ID（按时间排序最新的）"""
    if os.path.exists(MOVIE_JSON_PATH):
        try:
            with open(MOVIE_JSON_PATH, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                existing_movies = existing_data.get("movies", [])
                if existing_movies:
                    # 假设电影已经按时间排序，第一个就是最新的
                    return str(existing_movies[0]["id"])
        except Exception as e:
            print(f"读取现有数据时出错: {e}")
    return None

def fetch_douban_movies():
    """获取豆瓣电影数据"""
    all_movies = []
    # 对于PC版网页，起始索引应该从0开始
    start = 0
    page = 1
    has_more = True

    # 获取已有电影ID列表，避免重复获取
    existing_movie_ids = get_existing_movie_ids()
    print(f"已有电影数据 {len(existing_movie_ids)} 部")

    # 获取第一部电影的ID（如果存在）用于增量更新判断
    first_movie_id = get_first_movie_id()
    if first_movie_id:
        print(f"已有数据中第一部电影ID: {first_movie_id}，将用于增量更新判断")

    # 如果使用Selenium，初始化浏览器
    driver = None
    use_selenium = USE_SELENIUM
    if use_selenium:
        driver = init_selenium_driver()
        # 如果初始化失败，回退到requests方式
        if driver is None:
            use_selenium = False

    try:
        while has_more:
            # 使用PC版"看过"的电影页面
            url = f"https://movie.douban.com/people/{DOUBAN_UID}/collect?start={start}&sort=time&rating=all&filter=all&mode=grid"

            if use_selenium and driver:
                try:
                    movies_data, has_next_page, found_first_movie = fetch_page_movies_selenium(driver, url, page, existing_movie_ids, first_movie_id)
                except Exception as e:
                    print(f"Selenium获取失败，回退到requests方式: {e}")
                    movies_data, has_next_page, found_first_movie = fetch_page_movies(url, page, existing_movie_ids, first_movie_id)
            else:
                movies_data, has_next_page, found_first_movie = fetch_page_movies(url, page, existing_movie_ids, first_movie_id)

            # 无论是否找到第一部电影，都将当前页的新电影添加到结果中
            if movies_data:
                all_movies.extend(movies_data)

            if found_first_movie:
                print(f"在第 {page} 页找到已有数据中的第一部电影，增量更新完成")
                has_more = False
                break

            if not movies_data and not has_next_page:
                # 如果当前页没有获取到数据，且没有下一页，则结束循环
                has_more = False
                break
            elif not movies_data:
                # 如果当前页没有获取到数据，但有下一页，则继续
                start += PAGE_SIZE
                page += 1
                continue

            start += PAGE_SIZE
            page += 1
            has_more = has_next_page

            # 页面间随机延迟，避免请求过快
            time.sleep(random.uniform(2, 4))

        print(f"总共获取到 {len(all_movies)} 部新电影数据")
        return all_movies
    finally:
        # 确保关闭浏览器
        if driver:
            driver.quit()

def init_selenium_driver():
    """初始化Selenium WebDriver"""
    print("初始化Chrome浏览器...")
    try:
        options = Options()
        options.add_argument("--headless")  # 无头模式
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-software-rasterizer")

        # 添加随机UA
        # ua = UserAgent()
        # user_agent = ua.random
        # options.add_argument(f"user-agent={user_agent}")

        # 禁用自动化控制特征
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # 尝试使用本地已安装的Chrome浏览器
        try:
            # 首先尝试使用webdriver_manager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"使用webdriver_manager失败: {e}，尝试使用本地Chrome驱动...")
            # 如果webdriver_manager失败，尝试使用本地驱动
            chrome_driver_path = "D:\\chromedriver.exe"  # 请确保此路径正确
            service = Service(chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)

        # 设置页面加载超时
        driver.set_page_load_timeout(30)

        # 执行JavaScript来修改WebDriver特征
        driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """)

        print("Chrome浏览器初始化成功")
        return driver
    except Exception as e:
        print(f"初始化Chrome浏览器失败: {e}")
        print("将使用requests方式获取数据")
        return None

def fetch_page_movies_selenium(driver, url, page, existing_movie_ids, first_movie_id=None):
    """使用Selenium获取单页电影数据"""
    for retry in range(MAX_RETRIES):
        try:
            print(f"正在使用Selenium获取第 {page} 页电影数据...")

            # 访问页面
            driver.get(url)

            # 等待页面加载完成
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".grid-view .item"))
            )

            # 获取页面HTML
            html_content = driver.page_source

            # 检查是否包含"未登录无法查看更多内容"
            if "未登录无法查看更多内容" in html_content:
                print(f"检测到未登录提示，等待后重试...")
                # 刷新Cookie和UA
                # ua = UserAgent()
                # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua.random})
                # 清除所有cookie
                # driver.delete_all_cookies()
                # 添加随机cookie
                # driver.add_cookie({"name": "bid", "value": generate_random_bid(), "domain": ".douban.com"})
                time.sleep(RETRY_DELAY[retry] if retry < len(RETRY_DELAY) else 20)
                continue

            # 解析HTML响应
            return parse_html_response(html_content, page, existing_movie_ids, first_movie_id)

        except Exception as e:
            print(f"使用Selenium获取电影列表时出错: {e}，重试中...")
            time.sleep(RETRY_DELAY[retry] if retry < len(RETRY_DELAY) else 20)

    print(f"第 {page} 页数据获取失败，已达到最大重试次数")
    return [], False, False

def fetch_page_movies(url, page, existing_movie_ids, first_movie_id=None):
    """获取单页电影数据，带重试机制"""
    for retry in range(MAX_RETRIES):
        try:
            # 每次重试都使用新的随机User-Agent和Cookie
            ua = UserAgent(platforms='desktop')
            headers = {
                "User-Agent": ua.random,
                "Referer": "https://movie.douban.com/",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection": "keep-alive",
                "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "Cookie": get_random_cookie()  # 添加随机Cookie
            }

            print(f"正在获取第 {page} 页电影数据...")
            response = requests.get(url, headers=headers, timeout=10)

            # 打印响应状态和部分内容，帮助调试
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容前200字符: {response.text[:200]}")

            if response.status_code == 200:
                # 检查是否包含"未登录无法查看更多内容"
                if "未登录无法查看更多内容" in response.text:
                    print(f"检测到未登录提示，等待后重试...")
                    time.sleep(RETRY_DELAY[retry] if retry < len(RETRY_DELAY) else 20)
                    continue

                # 直接解析HTML响应
                return parse_html_response(response.text, page, existing_movie_ids, first_movie_id)

            elif response.status_code == 403 or response.status_code == 429:
                # IP可能被封，等待更长时间
                wait_time = RETRY_DELAY[retry] * 2 if retry < len(RETRY_DELAY) else 60
                print(f"请求被限制 (状态码: {response.status_code})，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"获取数据失败: {response.status_code}，重试中...")
                time.sleep(RETRY_DELAY[retry] if retry < len(RETRY_DELAY) else 20)

        except Exception as e:
            print(f"获取电影列表时出错: {e}，重试中...")
            time.sleep(RETRY_DELAY[retry] if retry < len(RETRY_DELAY) else 20)

    print(f"第 {page} 页数据获取失败，已达到最大重试次数")
    return [], False, False

def get_movie_details(movie_id, driver=None):
    """获取电影详细信息，带重试机制"""
    url = f"https://movie.douban.com/subject/{movie_id}/"

    # 如果提供了driver，尝试使用Selenium获取
    if driver and USE_SELENIUM:
        try:
            details = get_movie_details_selenium(driver, url, movie_id)
            if details:  # 如果成功获取到数据
                return details
            # 如果Selenium获取失败，回退到requests
            print(f"使用Selenium获取电影 {movie_id} 详情失败，回退到requests方式")
        except Exception as e:
            print(f"使用Selenium获取电影 {movie_id} 详情出错: {e}，回退到requests方式")

    # 使用requests获取
    for retry in range(MAX_RETRIES):
        try:
            # 添加随机延时
            time.sleep(random.uniform(1, 2))

            ua = UserAgent(platforms='desktop')
            headers = {
                "User-Agent": ua.random,
                "Referer": "https://movie.douban.com/",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection": "keep-alive",
                "Cookie": get_random_cookie()  # 添加随机Cookie
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 获取年份
                year = ""
                year_element = soup.select_one('.year')
                if year_element:
                    year_match = re.search(r'\((\d{4})\)', year_element.text)
                    if year_match:
                        year = year_match.group(1)

                # 获取导演
                director = ""
                director_element = soup.select_one('a[rel="v:directedBy"]')
                if director_element:
                    director = director_element.text.strip()

                # 获取简介
                description = ""
                summary_element = soup.select_one('span[property="v:summary"]')
                if summary_element:
                    description = summary_element.text.strip()
                # 如果上面的选择器没有找到，尝试另一个选择器
                if not description:
                    summary_element = soup.select_one('.related-info .indent span')
                    if summary_element:
                        description = summary_element.text.strip()

                # 获取豆瓣评分
                douban_rating = 0
                rating_element = soup.select_one('.rating_num')
                if rating_element:
                    try:
                        douban_rating = float(rating_element.text.strip())
                    except ValueError:
                        pass

                return {
                    "year": year,
                    "director": director,
                    "description": description,
                    "doubanRating": douban_rating
                }

            elif response.status_code == 403 or response.status_code == 429:
                # IP可能被封，等待更长时间
                wait_time = RETRY_DELAY[retry] * 2 if retry < len(RETRY_DELAY) else 60
                print(f"获取电影 {movie_id} 详情时请求被限制 (状态码: {response.status_code})，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"获取电影 {movie_id} 详情失败: {response.status_code}，重试中...")
                time.sleep(RETRY_DELAY[retry] if retry < len(RETRY_DELAY) else 20)

        except Exception as e:
            print(f"获取电影 {movie_id} 详情时出错: {e}，重试中...")
            time.sleep(RETRY_DELAY[retry] if retry < len(RETRY_DELAY) else 20)

    print(f"电影 {movie_id} 详情获取失败，已达到最大重试次数")
    return {}

def get_existing_movie_ids():
    """获取已有电影ID列表"""
    if os.path.exists(MOVIE_JSON_PATH):
        try:
            with open(MOVIE_JSON_PATH, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                existing_movies = existing_data.get("movies", [])
                return {str(movie["id"]) for movie in existing_movies}
        except Exception as e:
            print(f"读取现有数据时出错: {e}")
    return set()

def merge_with_existing_data(new_movies):
    """将新获取的电影数据与现有数据合并"""
    # 检查现有数据文件是否存在
    if os.path.exists(MOVIE_JSON_PATH):
        try:
            with open(MOVIE_JSON_PATH, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                existing_movies = existing_data.get("movies", [])

                # 创建现有电影ID的集合，用于检查新电影
                existing_movie_ids = {str(movie["id"]) for movie in existing_movies}
                
                # 筛选出真正的新电影（不在现有数据中的电影）
                truly_new_movies = [movie for movie in new_movies if str(movie["id"]) not in existing_movie_ids]
                
                # 将新电影放在最前面，然后是现有电影
                merged_movies = truly_new_movies + existing_movies
                
                return merged_movies
        except Exception as e:
            print(f"读取现有数据时出错: {e}")

    # 如果没有现有数据或读取出错，直接返回新数据
    return new_movies

def save_movies():
    """保存电影数据到JSON文件"""
    # 确保目录存在
    os.makedirs(os.path.dirname(MOVIE_JSON_PATH), exist_ok=True)

    # 获取新电影数据
    new_movies = fetch_douban_movies()

    if not new_movies:
        print("未获取到新电影数据")
        return

    # 合并现有数据
    merged_movies = merge_with_existing_data(new_movies)

    # 保存到JSON文件
    with open(MOVIE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"movies": merged_movies}, f, ensure_ascii=False, indent=2)

    print(f"已更新 {len(merged_movies)} 部电影到 {MOVIE_JSON_PATH}")

def parse_html_response(html_content, page, existing_movie_ids, first_movie_id=None, driver=None):
    """解析HTML响应内容"""
    soup = BeautifulSoup(html_content, 'html.parser')
    movies_data = []
    found_first_movie = False
    
    # 保存HTML以便调试
    # with open(f"douban_page_{page}.html", "w", encoding="utf-8") as f:
    #     f.write(html_content)
    # print(f"已保存页面HTML到douban_page_{page}.html用于调试")
    
    # 检查是否有下一页
    next_page = soup.select_one('span.next a')
    has_next_page = next_page is not None
    
    # 尝试不同的选择器
    movie_items = soup.select('.grid-view .item')
    if not movie_items:
        movie_items = soup.select('.list-view .item')
    
    if not movie_items:
        print(f"第 {page} 页没有找到电影数据，请检查HTML文件了解详情")
        return [], has_next_page, False
        
    # 处理电影项目
    for index, item in enumerate(movie_items, 1):
        try:
            # 获取电影链接和ID
            movie_link = item.select_one('.info .title a')
            if not movie_link:
                continue

            movie_url = movie_link['href']
            movie_id = re.search(r'subject/(\d+)/', movie_url).group(1)
            
            # 检查是否找到了第一部电影（用于增量更新）
            if first_movie_id and str(movie_id) == first_movie_id:
                print(f"找到已有数据中的第一部电影 (ID: {movie_id})，停止获取")
                found_first_movie = True
                break  # 直接跳出循环，不处理这部电影
            
            # 如果电影已存在于本地数据中，则跳过
            if str(movie_id) in existing_movie_ids:
                print(f"跳过已存在电影: {movie_link.text.strip()}")
                continue

            # 获取电影标题 - 只取第一个斜杠前的内容
            raw_title = movie_link.text.strip()
            title = raw_title.split('/')[0].strip()

            # 获取海报
            poster = ""
            poster_element = item.select_one('.pic img')
            if poster_element and 'src' in poster_element.attrs:
                poster = poster_element['src']

            # 获取我的评分和评论 - 参考get_movie.js的逻辑
            my_rating = 0
            comment = ""
            comment_element = item.select_one('.info .comment')
            if comment_element:
                comment = comment_element.text.strip()

                # 尝试从评语中提取评分
                try:
                    # 检查评论的第一部分是否为数字
                    first_part = comment.split('，')[0].strip()
                    temp_rating = float(first_part)

                    # 确保是有效的评分
                    if temp_rating and len(str(int(temp_rating))) == 1:  # 确保是单个数字
                        my_rating = temp_rating
                        # 如果是整数，补全为x.0格式
                        if my_rating == int(my_rating):
                            my_rating = float(f"{int(my_rating)}.0")
                except (ValueError, IndexError):
                    # 如果从评语中提取失败，尝试从rating元素提取
                    rating_element = item.select_one('[class^="rating"]')
                    if rating_element:
                        rating_class = rating_element.get('class')[0]
                        rating_match = re.search(r'rating(\d)-t', rating_class)
                        if rating_match:
                            star_count = int(rating_match.group(1))
                            my_rating = star_count * 2 - 1  # 计算评分
                            # 如果是整数，补全为x.0格式
                            if my_rating == int(my_rating):
                                my_rating = float(f"{int(my_rating)}.0")

            # 获取电影详情
            movie_details = get_movie_details(movie_id, driver)

            # 构建符合要求的电影数据结构
            movie = {
                "id": movie_id,
                "title": title,
                "year": movie_details.get("year", ""),
                "poster": poster,
                "description": movie_details.get("description", ""),
                "director": movie_details.get("director", ""),
                "doubanRating": movie_details.get("doubanRating", 0),
                "myRating": my_rating,
                "comment": comment,
                "url": movie_url
            }

            movies_data.append(movie)
            print(f"已获取第 {page} 页第 {index} 部电影: {movie['title']}, 评分: {my_rating}")

            # 如果这是已有数据中的第一部电影，处理完后停止
            if found_first_movie:
                break

            # 防止请求过快
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"处理电影项目时出错: {e}")
            continue
    
    return movies_data, has_next_page, found_first_movie

def get_directors_from_json(subject):
    """从JSON数据中提取导演信息"""
    directors = subject.get('directors', [])
    if directors:
        return ', '.join([d.get('name', '') for d in directors if 'name' in d])
    return ""

def get_movie_details_selenium(driver, url, movie_id):
    """使用Selenium获取电影详细信息"""
    for retry in range(MAX_RETRIES):
        try:
            print(f"使用Selenium获取电影 {movie_id} 详情...")

            # 访问页面
            driver.get(url)

            # 等待页面加载完成
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#content"))
            )

            # 获取页面HTML
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # 获取年份
            year = ""
            year_element = soup.select_one('.year')
            if year_element:
                year_match = re.search(r'\((\d{4})\)', year_element.text)
                if year_match:
                    year = year_match.group(1)

            # 获取导演
            director = ""
            director_element = soup.select_one('a[rel="v:directedBy"]')
            if director_element:
                director = director_element.text.strip()

            # 获取简介
            description = ""
            summary_element = soup.select_one('span[property="v:summary"]')
            if summary_element:
                description = summary_element.text.strip()
            # 如果上面的选择器没有找到，尝试另一个选择器
            if not description:
                summary_element = soup.select_one('.related-info .indent span')
                if summary_element:
                    description = summary_element.text.strip()

            # 获取豆瓣评分
            douban_rating = 0
            rating_element = soup.select_one('.rating_num')
            if rating_element:
                try:
                    douban_rating = float(rating_element.text.strip())
                except ValueError:
                    pass

            return {
                "year": year,
                "director": director,
                "description": description,
                "doubanRating": douban_rating
            }

        except Exception as e:
            print(f"使用Selenium获取电影 {movie_id} 详情时出错: {e}，重试中...")
            time.sleep(RETRY_DELAY[retry] if retry < len(RETRY_DELAY) else 20)

    print(f"电影 {movie_id} 详情获取失败，已达到最大重试次数")
    return {}

if __name__ == "__main__":
    save_movies()
