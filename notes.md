# ELK Day 01-02

## Setup
- docker compose up -d : containers start
- docker ps : chal rahe containers

## Dev Tools commands
- PUT students/_doc/1 {...} : ID ke saath document
- POST students/_update/1 {"doc": {...}} : partial update
- DELETE students/_doc/<id> : document hatao
- match query : analyzed search (case se farak nahi)
- term + name.keyword : exact search (case-sensitive)

## Seekha
- text vs keyword ka farak
- index ka naam galat likha to Elasticsearch naya index bana deta hai

since db :- with the use of since sb when we restart or update some filter in pipeline then it dont make any duplicate. 
/dev/null :- Book mark will be deleted automatically.
while saving the doc , at the end of the we must (enter),other wise it will not write (last line)

## Index templates and aggregation field names

**Idea:** a template is a mapping written in advance. Any new index whose name
matches `index_patterns` gets that mapping automatically.

**Without a template (dynamic mapping)**
- Elasticsearch guesses the type. Every string becomes `text` plus a
  `.keyword` sub-field.
- To aggregate or sort on `level`, I must write `level.keyword`.
- Two copies of every string are stored.

**With a template (I define `level` and `service` as `keyword`)**
- I write `"field": "level"` directly. No `.keyword`.
- Fields I did NOT put in the template (like `message`, `host.name`) are still
  dynamic, so they still need `.keyword`.
- A template only applies to NEW indices. To apply it to an existing index I
  must delete and reload it.

**What I never write in an aggregation:** the mapping type. I only write the
aggregation type (`terms`) and the field NAME. The type lives in the mapping.

**Wrong field name = no error, just empty buckets.**
- `level.keyword` after the template: empty (the sub-field does not exist)
- `message.keyword`: works (still dynamic)

**Habit:** run `GET <index>/_mapping` before writing a query.

### In my own words
- Why does a template make my queries shorter?
       because we dont need to write type , it is in already our templates.
- Why do `message` and `level` behave differently after the template?
         Because msg is a text and level is a keyword.



        Galti	Status	Result
Syntax galat (comma, quote, bracket tuta, querry)	400	Error, parsing_exception ya x_content_parse_exception
Index hi nahi hai (logstash_app_lgs)	404	Error, index_not_found_exception
Field ka naam galat (level.keyword jahan exist nahi karta)	200	Successful, par khaali

   Query	Kya aana chahiye	               Error ka naam
1. "querry" (spelling galat)	         400	parsing_exception ya x_content_parse_exception, unknown query jaisa message
2. logstash_app_lgs (index naam galat)	 404	index_not_found_exception, no such index
3. level.keyword (field naam galat)	     200, successful	Error nahi, buckets khaal