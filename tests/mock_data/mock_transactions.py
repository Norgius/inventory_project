from datetime import datetime, timedelta

two_days_ago = datetime.now().astimezone() - timedelta(days=2)
three_days_ago = datetime.now().astimezone() - timedelta(days=3)

mock_transactions = [
    {
      "user_id": 1,
      "product_id": 1,
      "amount": 100,
      "status": "completed",
      "created_at": two_days_ago,
    },
    {
      "user_id": 1,
      "product_id": 2,
      "amount": 500,
      "status": "completed",
      "created_at": two_days_ago,
    },
    {
      "user_id": 1,
      "product_id": 3,
      "amount": 80,
      "status": "completed",
      "created_at": two_days_ago,
    },
    {
      "user_id": 2,
      "product_id": 4,
      "amount": 750,
      "status": "completed",
      "created_at": two_days_ago,
    },
    {
      "user_id": 2,
      "product_id": 5,
      "amount": 50,
      "status": "completed",
      "created_at": three_days_ago,
    },
    {
      "user_id": 2,
      "product_id": 1,
      "amount": 100,
      "status": "completed",
      "purchased_at": three_days_ago,
    },
    {
      "user_id": 3,
      "product_id": 6,
      "amount": 300,
      "status": "completed",
      "created_at": three_days_ago,
    },
    {
      "user_id": 3,
      "product_id": 3,
      "amount": 80,
      "status": "completed",
      "created_at": three_days_ago,
    },
    {
      "user_id": 3,
      "product_id": 3,
      "amount": 80,
      "status": "completed",
      "created_at": two_days_ago,
    },
]
