import random

def get_system_metrics():
    
    return {
        "cpu_usage": round(random.uniform(20, 85), 2),
        "memory_usage": round(random.uniform(30, 90), 2),
        "active_users": random.randint(50, 300)
    }
