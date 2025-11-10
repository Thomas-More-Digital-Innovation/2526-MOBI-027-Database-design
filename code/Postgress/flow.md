```mermaid
flowchart TD
    A[CSV bestand push naar GitHub] --> B[GitHub Action triggered]
    B --> C[script CSV -> PostgreSQL]
    C --> D[(PosgreSQL - Neon DB)]
    D --> E[script Postgres -> Neo4j]
    E --> F(Neo4j Graph Database)]

```
