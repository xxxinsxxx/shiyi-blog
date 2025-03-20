import requests
import json
import time
import random
import os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # 需要安装: pip install fake-useragent

# 你的豆瓣 UID
DOUBAN_UID = "148921757"
MOVIE_JSON_PATH = "data/movies.json"  # 存放电影数据

def fetch_douban_movies():
    """获取豆瓣电影数据"""
    url = f"https://m.douban.com/rexxar/api/v2/user/{DOUBAN_UID}/interests?count=50&order_by=mark_time&status=done&type=movie&ck=&for_mobile=1"
    
    # 使用随机User-Agent
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Referer": "https://movie.douban.com/",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            movies_data = []
            
            for index, item in enumerate(data["interests"], 1):
                subject = item["subject"]
                movie_id = subject["id"]
                
                # 获取电影详情
                movie_details = get_movie_details(movie_id)
                
                # 构建符合要求的电影数据结构
                movie = {
                    "id": movie_id,
                    "title": subject["title"],
                    "year": subject.get("year", ""),
                    "poster": subject.get("cover_url", subject.get("cover", "")),
                    "description": movie_details.get("description", ""),
                    "director": movie_details.get("director", ""),
                    "doubanRating": subject.get("rating", {}).get("value", 0),
                    "myRating": item.get("rating", {}).get("value", 0),
                    "comment": item.get("comment", "")
                }
                
                movies_data.append(movie)
                print(f"已获取第 {index} 部电影: {movie['title']}")
                
                # 防止请求过快
                time.sleep(random.uniform(1, 2))
            
            return movies_data
        else:
            print("获取数据失败:", response.status_code)
            return []
    except Exception as e:
        print(f"获取电影列表时出错: {e}")
        return []

def get_movie_details(movie_id):
    """获取电影详细信息"""
    url = f"https://movie.douban.com/subject/{movie_id}/"
    
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Referer": "https://movie.douban.com/",
    }
    
    try:
        # 添加随机延时
        time.sleep(random.uniform(1, 2))
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"获取电影详情失败: {response.status_code}")
            return {}
        
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
        
        return {
            "director": director,
            "description": description
        }
    except Exception as e:
        print(f"获取电影详情时出错: {e}")
        return {}

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
        print("未获取到电影数据")
        return
    
    # 合并现有数据
    merged_movies = merge_with_existing_data(new_movies)
    
    # 保存到JSON文件
    with open(MOVIE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"movies": merged_movies}, f, ensure_ascii=False, indent=2)
    
    print(f"已更新 {len(merged_movies)} 部电影到 {MOVIE_JSON_PATH}")

if __name__ == "__main__":
    save_movies()