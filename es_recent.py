from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

res = es.search(

    index="app_logs",
    query={"range": {"@timestamp": {"gte": "now-15m", "lte": "now"}}},
    sort=[{"@timestamp": {"order": "desc"}}],
)

print("last 15min:", res["hits"]["total"]["value"])
for hit in res["hits"]["hits"]:
   s = hit["_source"]
   print(s["@timestamp"], s["level"], s["service"], s["message"])