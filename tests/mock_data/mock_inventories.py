from datetime import datetime, timedelta

two_days_ago = datetime.now().astimezone() - timedelta(days=2)
three_days_ago = datetime.now().astimezone() - timedelta(days=3)

mock_inventories = [
    {
      "user_id": 1,
      "product_id": 1,
      "quantity": 5,
      "purchased_at": two_days_ago
    },
    {
      "user_id": 1,
      "product_id": 2,
      "quantity": None,
      "purchased_at": two_days_ago
    },
    {
      "user_id": 1,
      "product_id": 3,
      "quantity": 3,
      "purchased_at": two_days_ago
    },
    {
      "user_id": 2,
      "product_id": 4,
      "quantity": None,
      "purchased_at": two_days_ago
    },
    {
      "user_id": 2,
      "product_id": 5,
      "quantity": 10,
      "purchased_at": three_days_ago
    },
    {
      "user_id": 2,
      "product_id": 1,
      "quantity": 2,
      "purchased_at": three_days_ago
    },
    {
      "user_id": 3,
      "product_id": 6,
      "quantity": None,
      "purchased_at": three_days_ago
    },
    {
      "user_id": 3,
      "product_id": 3,
      "quantity": 8,
      "purchased_at": three_days_ago
    },
    {
      "user_id": 3,
      "product_id": 5,
      "quantity": 15,
      "purchased_at": three_days_ago
    }
]
