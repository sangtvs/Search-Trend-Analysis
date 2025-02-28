from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import time

print("Waiting for Kafka to be ready...")
time.sleep(15)

consumer = KafkaConsumer('food_recipes_2024', bootstrap_servers='kafka:9092', auto_offset_reset='earliest')
client = MongoClient('mongo_db:27017')
db = client['holiday_db']
collection = db['recipes_2024']

print("Consumer started...")
count = 0
for message in consumer:
    data = json.loads(message.value.decode('utf-8'))
    collection.insert_one(data)
    count += 1
    if count % 5000 == 0:
        print(f"Inserted {count} records")
print(f"Consumer finished with {count} records.")