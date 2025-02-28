from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

recipes = [
    {"recipe": "Turkey Stuffing", "keywords": ["turkey", "Thanksgiving"], "location": "NYC", "timestamp": "2025-11-20"},
    {"recipe": "Christmas Cookies", "keywords": ["cookies", "Christmas"], "location": "NYC", "timestamp": "2025-12-24"}
]

# Tạo đủ dữ liệu (>300MB)
for _ in range(150000):  # ~300KB mỗi bản ghi JSON, cần ~1000 bản ghi cho 300MB, tăng lên nhiều hơn để chắc chắn
    for data in recipes:
        producer.send('nyc_holiday_recipes', value=data)
        print(f"Sent: {data}")
        time.sleep(0.001)  # Giả lập streaming

producer.flush()