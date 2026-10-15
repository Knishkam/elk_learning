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