# ELK Log Monitoring (Docker + Python)

A small log monitoring project. I generated synthetic application logs with
Python, stored them in Elasticsearch, and built a monitoring dashboard in Kibana.

![Dashboard](screenshots/dashboard.png)

## Stack
- Elasticsearch 8.15.0 and Kibana 8.15.0 (Docker Compose)
- Python 3 with the official `elasticsearch` client

## What is inside
| File | Purpose |
|---|---|
| `docker-compose.yml` | Runs Elasticsearch and Kibana locally (single node, security off for learning) |
| `es_gen.py` | Generates 200 synthetic logs (70% INFO, 20% WARN, 10% ERROR) and bulk-loads them |
| `es_bulk.py` | Bulk insert example using `helpers.bulk` |
| `es_queries.py` | Search with bool/range filters and terms aggregation |
| `es_recent.py` | Fetches logs from the last 15 minutes using `now-15m` |
| `queries.md` | Query DSL I practiced in Kibana Dev Tools |
| `notes.md` | My learning notes |

## Index mapping (`app_logs`)
| Field | Type |
|---|---|
| `@timestamp` | date |
| `level` | keyword |
| `service` | keyword |
| `status_code` | integer |
| `message` | text |

I defined the mapping explicitly, because a field's type cannot be changed
after the index is created without reindexing.

## How to run
1. Start the stack:
   ```
   docker compose up -d
   ```
2. Open Kibana at http://localhost:5601 (Dev Tools for queries)
3. Install the client and generate data:
   ```
   pip install "elasticsearch>=8,<9"
   python es_gen.py
   ```

## Dashboard
Four panels: total errors, logs over time, logs per service, recent logs table.

## Query DSL practiced
`match`, `term`, `terms`, `range`, `exists`, `match_phrase`, `multi_match`,
`bool` (must, filter, should, must_not), `highlight`, `sort`, `search_after`,
`terms` and `date_histogram` aggregations, Bulk API.

![Dev Tools](screenshots/devtools.png)

## What I learned
- (write 3-4 lines in your own words, for example: keyword fields are
  case-sensitive; why define mapping first; how the now-15m window works)

## Next
Logstash pipeline, Kibana alert rules, ILM
