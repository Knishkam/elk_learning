
GET app_logs/_search
{
  "size": 5,
  "sort": [
    { "@timestamp": { "order": "desc" } }
  ],
  "query": {
    "bool": {
      "must": [
        { "term": { "service.keyword": "payment" } },
        { "term": { "level.keyword": "ERROR" } },
        { "range": { "status_code": { "gte": 500 } } }
      ]
    }
  },
  "_source": ["@timestamp", "level", "message"]
}

GET app_logs/_search
{
  "size":5,
  "sort":[
    {"@timestamp": {"order": "desc"}}
    ],
  "query":{
    "bool": {
      "must":[
        { "term":{ "service": "payment"}},
        { "term": {"level": "ERROR"}},
        {"range": {"status_code": {
          "gte": 500}}}
        ]
    }
  },
  "_source": ["@timestamp", "level", "message"]
}



GET app_logs/_search
{
  "query": {
    "bool": {
      "should": [
        {"term": {
          "level": "ERROR"
          }
        },
        {"term": { "level" : "WARN"} }
      ],
      "minimum_should_match": 1,
      "must_not":[{"term":{"service": "auth"}}
    ]
  }
}}

GET app_logs/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "@timestamp": {
              "gte": "2026-10-01T00:00:00Z",
              "lte": "2026-10-31T23:59:59Z"
            }
          }
        },
        {
          "wildcard": {
            "message": {
              "value": "*slow*",
              "case_insensitive": true
            }
          }
        }
      ],
      "should": [
        {
          "wildcard": {
            "message": {
              "value": "*timeout*",
              "case_insensitive": true
            }
          }
        }
      ],
      "minimum_should_match": 1
    }
  }
}

GET app_logs/_search
{
  "size": 0,
  "aggs": {
    "by_service": {
      "terms": { "field": "service" },
      "aggs": {
        "by_level": {
          "terms": { "field": "level" }
        }
      }
    }
  }
}

GET app_logs/_search
{
  "size": 0,
  "aggs": {
    "by_service": {
      "terms": { "field": "service" },
      "aggs": {
        "by_level": {
          "terms": { "field": "level" }
        }
      }
    }
  }
}

GET app_logs/_search
{
  "size": 0,
  "aggs": {
    "logs_over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "fixed_interval": "30m"
      },
      "aggs": {
        "error_logs_only": {
          "filter": {
            "term": { "level": "ERROR" }
          }
        }
      }
    }
  }
}




GET app_logs/_search
{
  "size":0,
  "aggs": {
    "by_service":{
      "terms":{"field": "service"},
      "aggs":{
        "avg_status":{
          "avg": {
            "field": "status_code"}
        },
        "max_status": {
          "max": {"field": "status_code"}
        }
      }
    }
  }
}

 GET app_logs/_search
 { "query":{
   "bool": 
 { "should":
 { "term": { "level": "ERROR" } }}}}
 
 GET app_logs/_search 
 { "query": { "range": { "@timestamp": { "gte": "now-15m" } } } }



























