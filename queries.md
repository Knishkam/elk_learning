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
