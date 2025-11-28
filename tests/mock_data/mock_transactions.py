from datetime import datetime

mock_transactions = [
    {
      "user_id": 1,
      "product_id": 1,
      "amount": 100,
      "status": "completed",
      "created_at": datetime.fromisoformat("2024-02-15T11:00:00+03:00")
    },
    {
      "user_id": 1,
      "product_id": 2,
      "amount": 500,
      "status": "completed",
      "created_at": datetime.fromisoformat("2024-02-15T11:30:00+03:00")
    },
    {
      "user_id": 1,
      "product_id": 3,
      "amount": 80,
      "status": "completed",
      "created_at": datetime.fromisoformat("2024-02-16T09:45:00+03:00")
    },
    {
      "user_id": 2,
      "product_id": 4,
      "amount": 750,
      "status": "completed",
      "created_at": datetime.fromisoformat("2024-02-16T15:10:00+03:00")
    },
    {
      "user_id": 2,
      "product_id": 5,
      "amount": 50,
      "status": "completed",
      "created_at": datetime.fromisoformat("2024-02-16T15:15:00+03:00")
    },
    {
      "user_id": 3,
      "product_id": 6,
      "amount": 300,
      "status": "completed",
      "created_at": datetime.fromisoformat("2024-02-17T11:30:00+03:00")
    },
    {
      "user_id": 3,
      "product_id": 3,
      "amount": 80,
      "status": "completed",
      "created_at": datetime.fromisoformat("2024-02-18T08:45:00+03:00")
    }
]
