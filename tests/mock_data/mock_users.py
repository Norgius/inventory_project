from datetime import datetime, timedelta

five_days_ago = datetime.now().astimezone() - timedelta(days=5)
seven_days_ago = datetime.now().astimezone() - timedelta(days=7)

mock_users = [
    {
      "id": 1,
      "username": "Алисия",
      "email": "alice@example.com",
      "balance": 1500,
      "created_at": seven_days_ago
    },
    {
      "id": 2,
      "username": "Боб",
      "email": "bob@example.com",
      "balance": 800,
      "created_at": five_days_ago
    },
    {
      "id": 3,
      "username": "Черли",
      "email": "charlie@example.com",
      "balance": 2500,
      "created_at": five_days_ago
    }
]
