import random
from datetime import datetime, timedelta, timezone
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch("http://localhost:9200")

levels = ["INFO", "WARN", "ERROR"]
weights = [70, 20, 10]
services = ["auth", "payment", "api"]
messages = ["request ok", "slow response", "db timeout", "user login", "payment failed"]

now = datetime.now(timezone.utc)
actions = []

for _ in range(200):
    level = random.choices(levels, weights=weights, k=1)[0]
    service = random.choice(services)
    ts = now - timedelta(minutes=random.randint(0, 120))

    if level == "INFO":
        status = 200
    elif level == "WARN":
        status = 404
    else:
        status = 500

    actions.append({
        "_index": "app_logs",
        "_source": {
            "@timestamp": ts.isoformat(),
            "level": level,
            "service": service,
            "status_code": status,
            "message": random.choice(messages),
        },
    })

success, errors = helpers.bulk(es, actions)
print("inserted:", success, "errors:", errors)
print("total count:", es.count(index="app_logs")["count"])