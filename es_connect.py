from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")


print(es.ping())
print(es.info()["version"]["number"])

res = es.search(index="app_logs", query={"match_all": {}})
print(res["hits"]["total"]["value"])
