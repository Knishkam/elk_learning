GET _cluster/health
PUT students
POST students/_doc/2
{
  "name": "shivam",
  "age": 21,
  "city":"amethi"
}
PUT students/_settings
{
  "index": {
    "number_of_replicas": 0
  }
}
GET students/_search
PUT students/_doc/1
{
  "name": "RAHUL",
  "age": 65,
  "city": "kanpur"
}
GET students/_doc/1
DELETE students/_doc/nzBAPqEBvumEHXzNTC2w
GET students/_search
POST students/_update/1
{
  "doc":{
  "age": 23
  }
}
GET students/_doc/1
DELETE students/_doc/njA8PqEBvumEHXzNwS30
GET students/_doc/1
GET students/_search
{
  "query": { "match": { "city": "kanpur"} }
}
GET students/_search
{
  "query":{"match": {"name": "rahul"} }
}
GET students/_search
{
  "query": { "term": { "name.keyword": "rahul" }}
}
GEt students/_search
{
  "query": { "term": { "name.keyword": "RAHUL" }}
}

PUT app_logs
{
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "level": { "type": "keyword" },
      "service": { "type": "keyword" },
      "message": { "type": "text" },
      "status_code": { "type": "integer" }
    }
  }
}
GET app_logs/_mapping

GET app_logs/_search
{
  "query": {
    "term": { "level": "ERROR" }
  }
}

GET app_logs_nhi/_search
{
  "query" : {"term" : { "level" : "ERROR" } }
}

POST app_logs/_doc
{
  "@timestamp": "2026-10-15T10:30:00Z",
  "level": "warn",
  "service": "payment",
  "status_code": 500,
  "message": "all good"
}

POST app_logs/_doc
{
  "@timestamp": "2026-10-25T10:32:00Z",
  "level": "pass",
  "service": "operations",
  "status_code": 300,
  "message": "database received and saved"
}

POST app_logs/_doc
{
  "@timestamp": "2027-02-24T02:50Z",
  "level": "info",
  "service": "authorization",
  "status_codea": 2004,
  "message": "Payment done"
}

GET app_logs/_search
{
"query": { "term" : { "level": "pass" } }
}

GET app_logs/_search
{
  "query": { "match_all": {}}
}






GET app_logs/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "message": "database" } }
      ],
      "filter": [
        { "term": { "level": "pass" } },
        { "range": { "status_code": { "gte": 300 } } }
      ]
    }
  }
}

GET app_logs/_search
{
  "query": {
    "bool": {"filter": [
      {"term": { "level": "warn"}},
      { "range": { "status_code": { "gte": 300 }}}
    ]}
  }
}

GET app_logs/_search
{
  "query": {
    "bool": {
    "filter": [
      {
        "range": {"status_code": {"gte": 300}}
      }]
  }
}
  }

GET app_logs/_search
{
  "query": {
    "bool": {
      "should": [
        { "term": { "level": "warn" } },
        { "range": { "status_code": { "gte": 300 } } }
        
      ]
    }
  }
}

POST app_logs/_bulk
{"index": {}}
{"@timestamp": "2026-02-02T02:05Z", "level": "INFO", "service": "auth", "status_code": 200, "message": "message_linke_ok"}
{"index": {}}
{"@timestamp": "2026-04-05T05:20Z", "level": "ERROR", "service": "Warn", "status_code": 600, "message":"magic happening"}

GET app_logs/_search
{"query": {"match_all": {}}}















