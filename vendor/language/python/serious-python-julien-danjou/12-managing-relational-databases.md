# @Domain
These rules MUST trigger when the AI is tasked with creating, modifying, or reviewing Python code that interacts with relational databases, implements Object-Relational Mapping (ORM) tools (such as SQLAlchemy or Django ORM), designs SQL schemas, writes database migrations, handles data streaming/pub-sub systems linked to database changes, or structures Model-View-Controller (MVC) data access layers.

# @Vocabulary
- **RDBMS (Relational Database Management System):** A database that stores relational data and handles concurrency, isolation, atomicity, and data consistency.
- **ORM (Object Relational Mapping):** A library that abstracts database systems to generate SQL queries via object-oriented paradigms.
- **Object-Relational Impedance Mismatch:** The fundamental differences and friction between how relational databases model data and how object-oriented programming languages model objects.
- **Race Condition (in DB operations):** A vulnerability occurring when a program performs a `SELECT` to check for existence followed by an `INSERT`, allowing another thread/process to insert a conflicting record in between.
- **pl/pgsql:** The procedural language supported by PostgreSQL used to write trigger functions and native database scripts.
- **LISTEN / NOTIFY:** Native PostgreSQL features used for asynchronous pub-sub messaging directly from the database layer.
- **psycopg2:** A Python driver for PostgreSQL that implements the network protocol and allows low-level access to database features (such as `LISTEN`).
- **Server-Sent Events (SSE):** An HTML5 protocol for pushing data to a client via HTTP using the `text/event-stream` MIME type and a specific text format (`data: <payload>\n\n`).
- **CRUD:** Create, Read, Update, and Delete operations—the ideal use-case boundaries for simple ORM implementations.
- **Normalization:** The process of organizing a database schema to reduce redundancy and improve data integrity.
- **Denormalization:** The strategic inclusion of non-relational types (like composite types, arrays, H-Store, or JSON) inside an RDBMS, to be used strictly after proper normalization has proven insufficient for specific flexibility needs.

# @Objectives
- The AI MUST treat the RDBMS as a strict model API that enforces data integrity, not merely as dumb storage.
- The AI MUST eliminate database race conditions by delegating data constraints (e.g., uniqueness) strictly to the SQL layer and catching the resulting exceptions in Python.
- The AI MUST abstract and isolate ORM implementation details away from application business logic, views, and controllers.
- The AI MUST optimize ORM usage by retrieving only necessary columns to prevent severe scalability degradation.
- The AI MUST leverage native RDBMS features (like PostgreSQL's `LISTEN`/`NOTIFY` and JSON generation) for real-time data streaming instead of application-level polling loops.

# @Guidelines

### ORM Architecture & Isolation
- The AI MUST isolate all ORM logic into a dedicated module (e.g., `myapp.storage` or a `models` layer) that exports only high-level functions/methods.
- The AI MUST NOT leak ORM-specific query syntax or models into View or Controller code. Views/Controllers must call the storage module's abstract methods.
- The AI MUST use `sqlalchemy` as the default ORM and `alembic` for schema migrations in agnostic Python applications, unless a framework provides its own deeply integrated ORM (e.g., Django).
- The AI MUST restrict ORM queries to fetch *only* the specific columns needed for the operation. Querying full objects when only a few fields are needed is strictly forbidden.

### Data Integrity & Conflict Handling
- The AI MUST rely on SQL constraints (e.g., `PRIMARY KEY`, `UNIQUE`) to enforce data consistency.
- The AI MUST NOT implement a `SELECT`-then-`INSERT` pattern to check for duplicates. Instead, the AI MUST execute the `INSERT` directly and wrap it in a `try...except` block catching the specific unique violation error (e.g., `UniqueViolationError` or `IntegrityError`).

### Real-Time Data & Event Streaming
- When instructed to stream database changes, the AI MUST NOT implement polling (`while True: select...sleep`).
- The AI MUST use PostgreSQL `LISTEN` and `NOTIFY` features triggered by `pl/pgsql` database triggers.
- The AI MUST utilize database-native JSON casting (e.g., PostgreSQL's `row_to_json`) within the trigger function to format the payload before broadcasting.
- The AI MUST use a low-level driver like `psycopg2` combined with Python's `select.select()` module to asynchronously await `NOTIFY` events from the database without blocking.
- When serving streamed events over HTTP via frameworks like Flask, the AI MUST use a generator function yielding strings formatted as `"data: " + payload + "\n\n"` and set the HTTP response `mimetype` to `'text/event-stream'`.

### Schema Design & Types
- The AI MUST define explicit structure and constraints in the SQL schema (e.g., `NOT NULL`, `CHECK` constraints) rather than relying solely on Python-level validation.
- The AI MUST use strict relational mapping (Normalization) as the default. Denormalization (using JSON, Array, H-Store column types) MUST ONLY be used if dynamic flexibility is an explicit requirement that relational normalization cannot satisfy.

# @Workflow
When integrating relational databases or writing data-access layers, the AI MUST adhere to the following algorithmic process:
1. **Schema Definition:** Define the SQL schema with strict data types, primary keys, and necessary constraints (Unique, Check, Not Null).
2. **Layer Isolation:** Create a dedicated storage module (e.g., `storage.py`) to encapsulate all database interactions.
3. **Write Operations:** Implement insertions and updates using the `try...except` paradigm to catch database-enforced constraint violations.
4. **Read Operations:** Construct queries that explicitly select only the columns required by the calling code.
5. **Streaming Integration (If Applicable):**
   - Write a `CREATE FUNCTION` script in `pl/pgsql` using `pg_notify` and `row_to_json`.
   - Attach the function to the table via a `CREATE TRIGGER` script.
   - Establish a `psycopg2` connection in Python, set isolation level to `ISOLATION_LEVEL_AUTOCOMMIT`.
   - Execute a `LISTEN <channel>` cursor command.
   - Run an event loop using `select.select([conn], [], [])` and `conn.poll()`.
   - Extract events from `conn.notifies.pop()`.
   - Yield the payload wrapped in Server-Sent Events (SSE) format to the HTTP response.

# @Examples (Do's and Don'ts)

### Data Insertion and Race Condition Prevention
**[DON'T]** Use an ORM to check for existence before inserting (causes race conditions and redundant queries):
```python
# Anti-pattern: Select then Insert
if query.select(Message).filter(Message.id == some_id):
    raise DuplicateMessage(message)
else:
    query.insert(message)
```

**[DO]** Insert directly and catch the database constraint violation:
```python
# Best Practice: Let the RDBMS handle constraints
try:
    message_table.insert(message)
except UniqueViolationError:
    raise DuplicateMessage(message)
```

### Architectural ORM Isolation
**[DON'T]** Bleed ORM queries directly into a web route or controller:
```python
# Anti-pattern: Leaking ORM into the controller
@app.route("/users")
def get_users():
    # Controller knows about SQLAlchemy session and Model classes
    users = session.query(User.name, User.email).filter(User.active == True).all()
    return render_template("users.html", users=users)
```

**[DO]** Encapsulate the ORM inside a storage API:
```python
# Best Practice: Storage module abstraction
# storage.py
def get_active_users():
    return session.query(User.name, User.email).filter(User.active == True).all()

# views.py
import storage
@app.route("/users")
def get_users():
    users = storage.get_active_users()
    return render_template("users.html", users=users)
```

### Streaming Database Events via HTTP (Server-Sent Events)
**[DON'T]** Poll the database for new records to stream to a client:
```python
# Anti-pattern: Expensive polling loop
def stream_messages():
    last_id = 0
    while True:
        messages = session.query(Message).filter(Message.id > last_id).all()
        for msg in messages:
            last_id = msg.id
            yield f"data: {msg.content}\n\n"
        time.sleep(1)
```

**[DO]** Utilize PostgreSQL triggers, `LISTEN`/`NOTIFY`, and `psycopg2` with SSE formatting:
```sql
-- PostgreSQL Setup
CREATE OR REPLACE FUNCTION notify_on_insert() RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('channel_' || NEW.channel, CAST(row_to_json(NEW) AS TEXT));
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER notify_on_message_insert AFTER INSERT ON message
    FOR EACH ROW EXECUTE PROCEDURE notify_on_insert();
```
```python
# Python SSE streaming implementation
import flask
import psycopg2
import psycopg2.extensions
import select

app = flask.Flask(__name__)

def stream_messages(channel):
    conn = psycopg2.connect(database='mydb', user='user', password='pwd', host='localhost')
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    
    curs = conn.cursor()
    curs.execute("LISTEN channel_%d;" % int(channel))
    
    while True:
        select.select([conn], [], [])
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop()
            # Yield in Server-Sent Events (SSE) format
            yield "data: " + notify.payload + "\n\n"

@app.route("/message/<channel>", methods=['GET'])
def get_messages(channel):
    return flask.Response(stream_messages(channel), mimetype='text/event-stream')
```