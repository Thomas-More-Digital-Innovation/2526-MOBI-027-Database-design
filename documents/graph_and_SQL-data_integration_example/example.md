
# PostgreSQL + Apache AGE Example

This example demonstrates how to run PostgreSQL with the Apache AGE graph extension using Docker Compose.
It also includes pgAdmin as a web interface to manage the database and execute queries.

🧱 Setup

Start the containers:

docker compose up -d

Access pgAdmin at http://localhost:8080

Email: admin@admin.com
Password: admin

Add a new server with this information:

Host: postgres
Port: 5432
User: admin
Password: admin1234
Database: testdb

⚙️ Enable Apache AGE

In pgAdmin’s Query Tool, run:

LOAD 'age';
SET search_path = ag_catalog, "$user", public;

🧩 Example: Combining Graph and SQL Data

Create a regular SQL table:

CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO users (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com'),
('Charlie', 'charlie@example.com');

Create a graph and relationships:

SELECT create_graph('social_graph');

SELECT * FROM cypher('social_graph', $$
  CREATE (a:Person {name: 'Alice'})-[:KNOWS]->(b:Person {name: 'Bob'}),
         (b)-[:KNOWS]->(c:Person {name: 'Charlie'})
$$) AS (result agtype);

Join graph and SQL data:

SELECT u.name, u.email
FROM users u
JOIN LATERAL (
  SELECT * FROM cypher('social_graph', $$
    MATCH (p:Person) RETURN p.name AS name
  $$) AS (name text)
) g ON g.name = u.name;

✅ Result

This query links relational users table data with graph-based Person nodes —
demonstrating how Apache AGE allows seamless integration of SQL and graph data in one PostgreSQL instance.