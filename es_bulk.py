from datetime import datetime, timezone
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch("http://localhost:9200")
now = datetime.now(timezone.utc).isoformat()

actions = [
        {"_index": "app_logs", "_source": {"@timestamp": now, "level": "INFO",  "service": "auth",    "status_code": 200, "message": "login ok"}},
    {"_index": "app_logs", "_source": {"@timestamp": now, "level": "ERROR", "service": "payment", "status_code": 500, "message": "gateway timeout"}},
    {"_index": "app_logs", "_source": {"@timestamp": now, "level": "WARN",  "service": "auth",    "status_code": 429, "message": "too many attempts"}},
]
ok, errors = helpers.bulk(es, actions)
print("inserted:", ok, "errors:", errors)