from elasticsearch import Elasticsearch
from elasticsearch import ConnectionError as ESConnectionError

def a_client(url="http://localhost:9200"):
    return Elasticsearch(url)

def a_error_count(es, index="app_logs", minutes=15):
    res = es.count(
        index=index,
        query={"bool": {"filter": [
            {"term": {"level": "ERROR"}},
            {"range": { "@timestamp": {"gte": f"now-{minutes}m", "lte": "now"}}},
        ]}},
    )
    return res["count"]

def should_alert(count, threshold=3):
    return count >= threshold

def main():
    es = a_client()
    try:
        error_count = a_error_count(es)
    except ESConnectionError:
        print("Elasticsearch not reachable.")
        return
        print("Errors in last 15 min:", count)
        print("ALERT:" if should_alert(count) else "ALL GOOD")
if __name__ == "__main__":
    main()