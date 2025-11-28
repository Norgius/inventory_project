from datetime import datetime

mock_inventories = [
    {
      "user_id": 1,
      "product_id": 1,
      "quantity": 5,
      "purchased_at": datetime.fromisoformat("2024-02-15T11:00:00+03:00")
    },
    {
      "user_id": 1,
      "product_id": 2,
      "quantity": None,
      "purchased_at": datetime.fromisoformat("2024-02-15T11:30:00+03:00")
    },
    {
      "user_id": 1,
      "product_id": 3,
      "quantity": 3,
      "purchased_at": datetime.fromisoformat("2024-02-16T09:45:00+03:00")
    },
    {
      "user_id": 2,
      "product_id": 4,
      "quantity": None,
      "purchased_at": datetime.fromisoformat("2024-02-16T15:10:00+03:00")
    },
    {
      "user_id": 2,
      "product_id": 5,
      "quantity": 10,
      "purchased_at": datetime.fromisoformat("2024-02-16T15:15:00+03:00")
    },
    {
      "user_id": 2,
      "product_id": 1,
      "quantity": 2,
      "purchased_at": datetime.fromisoformat("2024-02-17T10:20:00+03:00")
    },
    {
      "user_id": 3,
      "product_id": 6,
      "quantity": None,
      "purchased_at": datetime.fromisoformat("2024-02-17T11:30:00+03:00")
    },
    {
      "user_id": 3,
      "product_id": 3,
      "quantity": 8,
      "purchased_at": datetime.fromisoformat("2024-02-18T08:45:00+03:00")
    },
    {
      "user_id": 3,
      "product_id": 5,
      "quantity": 15,
      "purchased_at": datetime.fromisoformat("2024-02-18T14:00:00+03:00")
    }
]
