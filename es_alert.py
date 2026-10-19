from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

res = es.count(
    index="app_logs",
    query={
        "bool": {
            "filter": [
                {"term": {"level": "ERROR"}},
                {"range": {"@timestamp": {"gte": "now-15m", "lte": "now"}}},
            ]
        }
    },
)

errors = res["count"]
print("errors in last 15 min:", errors)

if errors >= 1:
    print("ALERT: error aaya hai!")
else:
    print("sab theek hai")