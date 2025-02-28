# Search Trend Analysis for Food Recipes 2024

Phân tích xu hướng tìm kiếm công thức nấu ăn năm 2024 từ Google Trends và AllRecipes.

## Yêu cầu
- Docker và Docker Compose
- Internet để tải dữ liệu từ Google Trends và AllRecipes
- Python 3.9+

## Cấu trúc thư mục
- `docker-compose.yml`: Cấu hình dịch vụ Docker (MongoDB, Kafka, Spark, Jupyter)
- `Dockerfile.python`: Dockerfile cho dịch vụ python-app
- `requirements.txt`: Danh sách thư viện Python
- `jupyter_code/`: Chứa script producer và consumer
- `notebooks/`: Chứa notebook phân tích

## Cách chạy
1. **Clone dự án**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
2. **Chạy hệ thống Docker**:
   ```
    docker-compose up --build -d
4. **Tạo và streaming dữ liệu (nếu cần)**:
   ```
    docker-compose run python-app python jupyter_code/producer_2024.py
6. **Phân tích dữ liệu**:
   
    Mở http://localhost:8888, dùng token từ:
      ```
        docker-compose logs jupyter
      ```
    Mở notebooks/analysis_2024.ipynb và chạy.
