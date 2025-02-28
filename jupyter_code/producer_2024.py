from kafka import KafkaProducer
from pytrends.request import TrendReq
from bs4 import BeautifulSoup
import requests
import json
import time
import random

producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Khởi tạo pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Top 50 từ khóa công thức nấu ăn 2024
top_keywords = [
    "Olympic Chocolate Muffins", "Tanghulu", "Tini's Mac and Cheese", "Mama Kelce's Cookies", "Dense Bean Salad",
    "Chia Water", "Oatzempic", "Mango Pickle", "Dubai Chocolate Bar", "Cucumber Salad", "Marry Me Chicken",
    "Porn Star Martini", "Flat White Coffee", "Kanji Drink", "Maida Biscuit", "Chammanthi Podi", "Bitter Melon Soup",
    "Ema Datshi", "Sleepy Girl Mocktail", "Lemon Balm Tea", "Grinder Sandwich", "Chopped Italian Sandwich",
    "Cottage Cheese Toast", "Baked Feta Pasta", "Sushi Bake", "Air Fryer Chicken Wings", "Viral Spaghetti",
    "Korean Corn Dogs", "Smash Burgers", "Birria Tacos", "Cloud Bread", "Whipped Coffee", "Focaccia Bread",
    "Sourdough Starter", "Banana Bread", "Chili Crunch Oil", "Hot Honey Chicken", "Pesto Eggs", "Bowl Meals",
    "Sheet Pan Dinner", "One Pot Pasta", "Instant Pot Ribs", "Vegan Brownies", "Keto Pancakes", "Gluten Free Pizza",
    "Matcha Latte", "Acai Bowl", "Protein Shake Recipes", "Charcuterie Board", "Truffle Fries"
]

print("Fetching Google Trends data and scraping recipes...")
recipe_data = []

# Thu thập dữ liệu từ Google Trends và AllRecipes
for i, kw in enumerate(top_keywords):
    try:
        # Lấy dữ liệu từ Google Trends
        pytrends.build_payload([kw], timeframe='2024-01-01 2024-12-31', geo='US')
        interest_over_time = pytrends.interest_over_time()
        if not interest_over_time.empty:
            search_vol = int(interest_over_time[kw].mean() * 100)  # Quy đổi tương đối
        else:
            search_vol = random.randint(100, 1000)  # Giá trị mặc định nếu không có dữ liệu
            print(f"No Trends data for {kw}, using default search_vol: {search_vol}")

        # Scraping công thức từ AllRecipes
        url = f"https://www.allrecipes.com/search?q={kw.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        recipe_link = soup.find('a', class_='card__titleLink')
        if recipe_link:
            recipe_url = recipe_link['href']
            recipe_response = requests.get(recipe_url, headers=headers)
            recipe_soup = BeautifulSoup(recipe_response.text, 'html.parser')
            ingredients = [li.text.strip() for li in recipe_soup.find_all('li', class_='ingredient')]
            if not ingredients:
                ingredients = kw.split()  # Fallback nếu không tìm thấy
                print(f"No ingredients found for {kw}, using fallback: {ingredients}")
        else:
            ingredients = kw.split()
            print(f"No recipe link found for {kw}, using fallback: {ingredients}")

        entry = {
            "id": f"recipe_{i}",
            "keyword": kw,
            "search_vol": search_vol,
            "recipe": ingredients
        }
        recipe_data.append(entry)
        print(f"Processed {kw}: {search_vol} searches, {len(ingredients)} ingredients")
        time.sleep(2)  # Tránh bị chặn
    except Exception as e:
        print(f"Error processing {kw}: {str(e)}")
        continue

print(f"Collected {len(recipe_data)} unique recipes")

# Mở rộng thành 50,000 bản ghi
print("Expanding to 50,000 records...")
for i in range(50000):
    base_data = random.choice(recipe_data)  # Chọn ngẫu nhiên từ danh sách đã thu thập
    data = {
        "id": f"recipe_2024_{i}",
        "keyword": base_data["keyword"],
        "search_vol": base_data["search_vol"] + random.randint(-50, 50),  # Biến động nhỏ
        "recipe": base_data["recipe"]
    }
    producer.send('food_recipes_2024', value=data)
    if i % 5000 == 0:
        print(f"Sent {i} records...")
    time.sleep(0.001)

producer.flush()
print("Producer finished.")