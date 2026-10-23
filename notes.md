# ELK Learning Notes (Days 01-03)

> Elasticsearch is a giant, very fast library. Kibana is the reading room window.
> Python is my robot librarian. These notes are what I learned building a
> log monitoring dashboard from scratch.

---

## 1. Docker: my toolbox

Docker runs Elasticsearch and Kibana in sealed boxes called **containers**.
A `docker-compose.yml` is the recipe that says which boxes to run.

| Command | What it does |
|---|---|
| `docker compose up -d` | Read the recipe, start everything in the background |
| `docker ps` | Which boxes are running right now (`-a` includes stopped ones) |
| `docker compose logs <service> --tail 30` | The box's diary, last 30 lines |
| `docker compose stop` | Switch off the boxes, my data stays safe |
| `docker compose down -v` | Delete the boxes AND the data volume. Careful! |

**Things that bit me**
- `depends_on` only controls *start order*, not "is it actually ready". After a
  restart, Kibana can say "not ready" or return a 500 for a minute or two. Wait.
- Memory: I set the Java heap to 1 GB (`ES_JAVA_OPTS=-Xms1g -Xmx1g`) because my
  laptop has 8 GB RAM.
- Keep the Elasticsearch and Kibana versions identical (8.15.0).
- A **volume** keeps data outside the container, so deleting the container
  does not delete my logs.

---

## 2. The basic vocabulary

| Elasticsearch | Think of it as |
|---|---|
| Index | A table (or a bookshelf) |
| Document | One row (one book), stored as JSON |
| Shard | One slice of the bookshelf |
| Replica | A backup copy of a slice |
| Inverted index | The index at the back of a book: word -> which pages |

**Writing data**
- `PUT index/_doc/1` -> I choose the ID. Running it again *replaces* the
  document (same result every time).
- `POST index/_doc` -> Elasticsearch invents the ID. Run it twice and I get
  **two** documents (duplicates).
- If an index does not exist, Elasticsearch creates it automatically.
  So a typo in the index name quietly creates a brand new wrong index.
- `_update` changes only some fields: `{"doc": {"age": 23}}`.
- On a single node, replicas have no place to live, so the cluster shows
  **yellow**. Setting replicas to 0 makes it **green**. Not an error.

---

## 3. text vs keyword (the most important idea)

| | `text` | `keyword` |
|---|---|---|
| Analyzed? | Yes: split into words, lowercased | No: stored exactly as written |
| Search with | `match` | `term` (exact, **case-sensitive**) |
| Use for | Free text: `message` | Exact values: `level`, `service` |

- `INFO` and `info` are two different keywords. A dashboard would count them
  separately and show wrong numbers.
- `keyword` is also needed for sorting and aggregations.
- A field's type **cannot be changed** after creation (you must reindex),
  so I design the mapping first.
- If I skip the mapping, Elasticsearch guesses and often creates both `text`
  and `.keyword` for every string (wasteful).

### In my own words
- What `text` does: It is used for exact search (it converted into lowercase) and it is casesensitive.
- What `keyword` does: It is used for exact save and it is case sensitive.
- Why `term` for "rahul" did not find "RAHUL": while searching it will search RAHUL but as its attributes it saves in lowercase.
- Why `level` should be a keyword in log monitoring: level (warn , pass, fail ) should be case sensitive  and we need exact search .

---

## 4. Query DSL: the sieve

A query is a sieve: only documents that fit the shape fall through.

**Basic queries**
- `match`: analyzed search, case does not matter
- `match_phrase`: words must appear in that order
- `multi_match`: one text, many fields.
  `query` = *what* to find, `fields` = *where* to look
- `term` / `terms` (any of several values): exact match on keywords
- `exists`: the field is present (`field` takes one name, not a list)
- `range`: `gte` (>=), `lte` (<=), `gt`, `lt`
- `match_all`: no condition, everything passes

**`bool`: combining conditions**

| Clause | Meaning | Affects score? |
|---|---|---|
| `must` | Must match (AND) | Yes |
| `filter` | Must match (AND) | No |
| `should` | Nice to match (OR) | Yes |
| `must_not` | Must NOT match | No |

- `should` and `must` are not queries by themselves, they live *inside* `bool`.
- If `should` sits next to `must` or `filter`, it becomes optional (it only
  boosts the score). If it is alone, at least one must match.
  Writing `minimum_should_match: 1` makes the intention clear.
- Nested `bool` = an OR inside an AND.

**Shaping the results**
- `size` (default 10), `sort`, `_source` (pick fields), `highlight` (wraps
  matches in `<em>`)
- `search_after`: pagination for big data. Repeat the same sort and pass the
  `sort` values of the last hit. `_doc` is used as a tie-breaker.
  (For production, read about point-in-time. Verify in the docs.)

---

## 5. Dates and time

- Elasticsearch compares the full timestamp and stores it in UTC.
- `now-15m` is recalculated **every time the query runs**, so the same query
  returns fewer hits as time passes (it returned 0 for me 15 minutes later).
- Always give both ends: `gte: now-15m`, `lte: now`. With only `gte`, documents
  with future timestamps sneak in.
- Documents outside Kibana's time picker simply do not show up in charts.

---

## 6. Aggregations: the calculator

Search returns documents. Aggregations return **answers**.

- `"size": 0` = I only want the numbers.
- `terms`: count per value (`key`, `doc_count`)
- `avg`, `min`, `max`: maths on numbers
- Sub-aggregation: an `aggs` inside an `aggs` (per service, then per level)
- `date_histogram`: buckets over time (`calendar_interval` for months/days,
  `fixed_interval` for 30m)
- Without a query, an aggregation runs on **all** documents. With a query, only
  on the documents that survive it.

---

## 7. Bulk API: loading in bulk

- Format: an action line, then a document line, each on **one line**, and an
  empty line at the end. No commas between lines.
- Always check `"errors": false`. If one document fails, the others still go in.
- Python: `ok, errors = helpers.bulk(es, actions)`
- Running bulk again adds documents again (no IDs, so duplicates).

---

## 8. Reading errors

| Status | Meaning |
|---|---|
| 400 | My request is wrong (parse error, unknown key). Look at `[line:column]` |
| 404 | Index or document not found |
| 500 | Server-side problem (e.g. shards still loading after a restart) |

- Typo in a **keyword** (`querry`) -> 400 error.
- Typo in a **field name** (`stasus_code`) -> **no error**, just 0 hits.
- The parser stops at the first mistake, so fixing one reveals the next.
- Shards "successful: 1" means the search ran, not that it found anything.

---

## 9. Python client

- Client major version must match the server (mine: server 8.15, client 8.x).
- `es.ping()`, `es.info()`, `es.search(index, query, size, sort, aggs)`,
  `es.count()`
- The response is a dictionary: `res["hits"]["total"]["value"]`,
  `hit["_source"]["level"]`
- Dev Tools JSON becomes a Python dictionary.

---

## 10. Kibana

- **Data View** = index pattern + time field (`@timestamp`).
- One chart answers one question. Layers are only for comparing things on
  the same axes.
- My dashboard: Total ERRORS (metric, KQL `level : "ERROR"`), Logs over time,
  Logs per service, Recent logs.

---

## My mistakes (and what they taught me)

| Mistake | Lesson |
|---|---|
| Missing comma / colon | JSON parse error, read `[line:column]` |
| `querry` spelling | Unknown key -> 400 |
| Wrote to index `update` by accident | Wrong index name = silent new index |
| Bulk action split over 3 lines | Bulk needs one JSON per line |
| File named `es_connect.pya` | One extra letter, Python ignores it |


