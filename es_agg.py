from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

res = es.search(
    index="app_logs",
    size=0,
    aggs={
        "per_service": {
            "terms": {"field": "service"},
            "aggs": {"per_level": {"terms": {"field": "level"}}},
        },
        "per_month": {
            "date_histogram": {"field": "@timestamp", "calendar_interval": "month"}
        },
    },
)

for s in res["aggregations"]["per_service"]["buckets"]:
    print(s["key"], s["doc_count"])
    for l in s["per_level"]["buckets"]:
        print("   ", l["key"], l["doc_count"])

for m in res["aggregations"]["per_month"]["buckets"]:
    print(m["key_as_string"], m["doc_count"])