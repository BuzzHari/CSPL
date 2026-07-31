# DS-002 — The Google File System

- **Authors:** Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung
- **Year:** 2003
- **Field:** Distributed Systems / Distributed Storage
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://research.google/pubs/the-google-file-system/

## Why it matters

GFS established a practical distributed-storage architecture based on commodity machines, large files, replication, relaxed consistency, and the assumption that failures are normal.

## Key ideas

1. Workload-driven system design
2. Separation of metadata from bulk data
3. Large chunks
4. Replication and continuous recovery
5. Primary leases for mutation ordering

## Work connection

Relevant to storing logs, packet captures, crash dumps, core dumps, and other large diagnostic artifacts collected from device fleets.
