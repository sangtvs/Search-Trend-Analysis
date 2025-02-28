from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import time

# Thêm độ trễ để đợi Kafka
print("Waiting for Kafka to be ready...")
time.sleep(10)  # Đợi 10 giây

consumer = KafkaConsumer('nyc_holiday_recipes', bootstrap_servers='kafka:9092', auto_offset_reset='earliest')
client = MongoClient('mongo_db:27017')
db = client['holiday_db']
collection = db['holiday_recipes']

for message in consumer:
    data = json.loads(message.value.decode('utf-8'))
    if "NYC" in data["location"]:
        collection.insert_one(data)
        print(f"Inserted: {data}")