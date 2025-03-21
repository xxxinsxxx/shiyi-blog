import requests
import json
import time
import random
import os
import re
import string
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # 需要安装: pip install fake-useragent

# 你的豆瓣 UID
DOUBAN_UID = "148921757"
MOVIE_JSON_PATH = "public/movies.json"  # 存放电影数据
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = [5, 10, 20]  # 重试延迟时间（秒）
PAGE_SIZE = 15  # 每页电影数量

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

def fetch_douban_movies():
    """获取豆瓣电影数据"""
    all_movies = []
    start = 1
    page = 1
    has_more = True

    # 获取已有电影ID列表，避免重复获取
    existing_movie_ids = get_existing_movie_ids()
    print(f"已有电影数据 {len(existing_movie_ids)} 部")

    while has_more:
        # 使用PC版"看过"的电影页面
        url = f"https://movie.douban.com/people/{DOUBAN_UID}/collect?start={start}&sort=time&rating=all&filter=all&mode=grid"

        movies_data, has_next_page = fetch_page_movies(url, page, existing_movie_ids)

        if not movies_data:
            # 如果当前页没有获取到数据，可能是到达末尾或者出错
            if not has_next_page:
                has_more = False
                break
            else:
                # 尝试下一页
                start += PAGE_SIZE
                page += 1
                continue

        all_movies.extend(movies_data)
        start += PAGE_SIZE
        page += 1
        has_more = has_next_page

        # 页面间随机延迟，避免请求过快
        time.sleep(random.uniform(2, 4))

    print(f"总共获取到 {len(all_movies)} 部新电影数据")
    return all_movies

def fetch_page_movies(url, page, existing_movie_ids):
    """获取单页电影数据，带重试机制"""
    for retry in range(MAX_RETRIES):
        try:
            # 使用随机User-Agent
            ua = UserAgent()
            headers = {
                "User-Agent": ua.random,
                "Referer": "https://movie.douban.com/",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cookie": get_random_cookie()  # 添加随机Cookie
            }

            print(f"正在获取第 {page} 页电影数据...")
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                movies_data = []

                # 检查是否有下一页
                next_page = soup.select_one('span.next a')
                has_next_page = next_page is not None

                # 获取电影项目列表
                movie_items = soup.select('.grid-view .item')

                if not movie_items:
                    print(f"第 {page} 页没有找到电影数据")
                    return [], has_next_page

                for index, item in enumerate(movie_items, 1):
                    try:
                        # 获取电影链接和ID
                        movie_link = item.select_one('.info .title a')
                        if not movie_link:
                            continue

                        movie_url = movie_link['href']
                        movie_id = re.search(r'subject/(\d+)/', movie_url).group(1)

                        # 如果电影已存在于本地数据中，则跳过
                        if str(movie_id) in existing_movie_ids:
                            print(f"跳过已存在电影: {movie_link.text.strip()}")
                            continue

                        # 获取电影标题
                        title = movie_link.text.strip()

                        # 获取海报
                        poster = ""
                        poster_element = item.select_one('.pic img')
                        if poster_element and 'src' in poster_element.attrs:
                            poster = poster_element['src']

                        # 获取年份
                        year = ""
                        year_match = re.search(r'\((\d{4})\)', item.select_one('.info .title').text)
                        if year_match:
                            year = year_match.group(1)

                        # 获取我的评分
                        my_rating = 0
                        rating_element = item.select_one('.info .date + span')
                        if rating_element:
                            rating_match = re.search(r'rating(\d+)-t', str(rating_element))
                            if rating_match:
                                my_rating = int(rating_match.group(1))

                        # 获取评论
                        comment = ""
                        comment_element = item.select_one('.info .comment')
                        if comment_element:
                            comment = comment_element.text.strip()

                        # 获取电影详情
                        movie_details = get_movie_details(movie_id)

                        # 构建符合要求的电影数据结构
                        movie = {
                            "id": movie_id,
                            "title": title,
                            "year": year,
                            "poster": poster,
                            "description": movie_details.get("description", ""),
                            "director": movie_details.get("director", ""),
                            "doubanRating": movie_details.get("doubanRating", 0),
                            "myRating": my_rating,
                            "comment": comment,
                            "url": movie_url
                        }

                        movies_data.append(movie)
                        print(f"已获取第 {page} 页第 {index} 部电影: {movie['title']}")

                        # 防止请求过快
                        time.sleep(random.uniform(1, 2))
                    except Exception as e:
                        print(f"处理电影项目时出错: {e}")
                        continue

                return movies_data, has_next_page

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
    return [], False

def get_movie_details(movie_id):
    """获取电影详细信息，带重试机制"""
    url = f"https://movie.douban.com/subject/{movie_id}/"

    for retry in range(MAX_RETRIES):
        try:
            # 添加随机延时
            time.sleep(random.uniform(1, 2))

            ua = UserAgent()
            headers = {
                "User-Agent": ua.random,
                "Referer": "https://movie.douban.com/",
                "Cookie": get_random_cookie()  # 添加随机Cookie
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

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

                # 获取豆瓣评分
                douban_rating = 0
                rating_element = soup.select_one('.rating_self strong')
                if rating_element:
                    try:
                        douban_rating = float(rating_element.text.strip())
                    except ValueError:
                        pass

                return {
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

                # 创建现有电影ID的映射
                existing_movie_map = {str(movie["id"]): movie for movie in existing_movies}

                # 合并新电影数据，优先使用新数据
                for movie in new_movies:
                    existing_movie_map[str(movie["id"])] = movie

                # 转换回列表
                merged_movies = list(existing_movie_map.values())

                # 按ID排序
                merged_movies.sort(key=lambda x: str(x["id"]))

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

if __name__ == "__main__":
    save_movies()
