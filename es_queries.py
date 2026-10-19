from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
res = es.search(index="app_logs", query={
    "bool": {
"filter":[
{"range": {"status_code":{"gte": 300}}}
]
    }
},
size=10,
)
print("total:", res["hits"]["total"]["value"])
for hit in res["hits"]["hits"]:
    print(hit["_id"], hit["_source"]["level"], hit["_source"]["message"]
    )
agg = es.search(index="app_logs", size=0, aggs={"logs_per_level": {"terms": {"field": "level"}}},
)
for b in agg["aggregations"]["logs_per_level"]["buckets"]:
    print(b["key"], b["doc_count"])
