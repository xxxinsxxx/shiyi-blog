import json
import time
import random
import os
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# 配置参数
MOVIE_JSON_PATH = "data/movies.json"  # 存放电影数据
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = [5, 10, 20]  # 重试延迟时间（秒）

def generate_random_bid():
    """生成随机的豆瓣bid"""
    # bid格式为11位字母数字组合
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(11))

def get_random_cookie():
    """获取带有随机bid的Cookie"""
    bid = generate_random_bid()
    return f'bid={bid};dbcl2="148921757:4OH+mZkQeUM"; '

def get_movie_details(movie_id):
    """获取电影详细信息，带重试机制"""
    url = f"https://movie.douban.com/subject/{movie_id}/"

    for retry in range(MAX_RETRIES):
        try:
            # 添加随机延时
            time.sleep(random.uniform(1, 2))

            ua = UserAgent(platforms='desktop')
            headers = {
                "User-Agent": ua.random,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
                "Cookie": get_random_cookie()  # 添加随机Cookie
            }

            response = requests.get(url, headers=headers, timeout=10)
            print(f"已保存电影 {response} 的HTML到 {url}")
            if response.status_code == 200:
                # 保存HTML以便检查
                # html_dir = "douban_html"
                # os.makedirs(html_dir, exist_ok=True)
                # with open(f"{html_dir}/movie_{movie_id}.html", "w", encoding="utf-8") as f:
                #     f.write(response.text)
                # print(f"已保存电影 {movie_id} 的HTML到 {html_dir}/movie_{movie_id}.html")

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

def load_movies():
    """加载现有电影数据"""
    if os.path.exists(MOVIE_JSON_PATH):
        try:
            with open(MOVIE_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("movies", [])
        except Exception as e:
            print(f"读取电影数据时出错: {e}")
            return []
    else:
        print(f"电影数据文件 {MOVIE_JSON_PATH} 不存在")
        return []

def save_movies(movies):
    """保存电影数据"""
    # 确保目录存在
    os.makedirs(os.path.dirname(MOVIE_JSON_PATH), exist_ok=True)

    with open(MOVIE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"movies": movies}, f, ensure_ascii=False, indent=2)

    print(f"已保存 {len(movies)} 部电影到 {MOVIE_JSON_PATH}")

def is_detail_missing(movie):
    """检查电影是否缺少详细信息"""
    # 检查年份、导演、描述或豆瓣评分是否为空
    return (
        not movie.get("year") or
        not movie.get("director") or
        not movie.get("description") or
        not movie.get("doubanRating")
    )

def fix_movie_details():
    """修复电影详细信息"""
    movies = load_movies()
    if not movies:
        print("没有找到电影数据")
        return

    total_movies = len(movies)
    missing_details_count = 0
    fixed_count = 0

    print(f"开始检查 {total_movies} 部电影的详细信息...")

    for i, movie in enumerate(movies):
        movie_id = movie.get("id")
        title = movie.get("title")

        if is_detail_missing(movie):
            missing_details_count += 1
            print(f"[{i+1}/{total_movies}] 电影 '{title}' (ID: {movie_id}) 缺少详细信息，正在获取...")

            # 获取详细信息
            details = get_movie_details(movie_id)

            if details:
                # 更新电影信息
                if not movie.get("year") and details.get("year"):
                    movie["year"] = details["year"]
                    print(f"  - 已更新年份: {details['year']}")

                if not movie.get("director") and details.get("director"):
                    movie["director"] = details["director"]
                    print(f"  - 已更新导演: {details['director']}")

                if not movie.get("description") and details.get("description"):
                    movie["description"] = details["description"]
                    print(f"  - 已更新描述")

                if not movie.get("doubanRating") and details.get("doubanRating"):
                    movie["doubanRating"] = details["doubanRating"]
                    print(f"  - 已更新豆瓣评分: {details['doubanRating']}")

                fixed_count += 1
            else:
                print(f"  - 无法获取详细信息")

            # 随机延迟，避免请求过快
            time.sleep(random.uniform(2, 4))
        else:
            print(f"[{i+1}/{total_movies}] 电影 '{title}' (ID: {movie_id}) 详细信息完整，跳过")

    print(f"\n检查完成: 共 {total_movies} 部电影，{missing_details_count} 部缺少详细信息，成功修复 {fixed_count} 部")

    if fixed_count > 0:
        # 保存更新后的电影数据
        save_movies(movies)
    else:
        print("没有电影需要更新，跳过保存")

if __name__ == "__main__":
    fix_movie_details()
