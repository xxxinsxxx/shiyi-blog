import requests
import json

# 你的豆瓣 UID
DOUBAN_UID = "148921757"
MOVIE_JSON_PATH = "public/movies.json"  # 存放电影数据

def fetch_douban_movies():
    url = f"https://m.douban.com/rexxar/api/v2/user/{DOUBAN_UID}/interests?count=50&order_by=mark_time&status=done&ck=&for_mobile=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        movies = [
            {
                "title": item["subject"]["title"],
                "url": f"https://movie.douban.com/subject/{item['subject']['id']}/",
                "cover": item["subject"]["cover"],
                "rating": item["subject"].get("rating", {}).get("value", "N/A"),
                "mark_time": item["create_time"]
            }
            for item in data["interests"]
        ]
        return movies
    else:
        print("获取数据失败:", response.status_code)
        return []

def save_movies():
    movies = fetch_douban_movies()
    with open(MOVIE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)
    print(f"已更新 {len(movies)} 部电影")

if __name__ == "__main__":
    save_movies()
