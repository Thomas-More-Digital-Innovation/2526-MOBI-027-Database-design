```mermaid
flowchart TD
    A[CSV bestand push naar GitHub] --> B[GitHub Action triggered]
    B --> C[script CSV -> PostgreSQL]
    C --> D[script Postgres -> Neo4j]
    D --> E[(Neo4j Graph Database)]

```
