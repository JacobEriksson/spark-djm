import json
import time
import random
import os

output_dir = "/mnt/data/orders"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

product_ids = ["101", "102", "103"]

def generate_order():
    return {
        "orderId": random.choice(product_ids),
        "customerId": str(random.randint(2000, 2999)),
        "amount": random.randint(1, 50),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

try:
    while True:
        file_path = os.path.join(output_dir, f"order_{int(time.time())}.json")
        with open(file_path, "w") as file:
            order = generate_order()
            file.write(json.dumps(order) + "\n")
            print (f"Order placed as {file_path}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Order generation stopped.")
