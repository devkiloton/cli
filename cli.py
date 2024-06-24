import mysql.connector as mysql
import argparse

def create_connection(text):
    # Get arguments
    input = text.split("connect ")[1]

    # Parse arguments
    parser_db_connection = argparse.ArgumentParser()
    parser_db_connection.add_argument('--user', dest='user', type=str, help='Add mysql database user')
    parser_db_connection.add_argument('--password', dest='password', type=str, help='Add mysql database password')
    parser_db_connection.add_argument('--host', dest='host', type=str, help='Add mysql database host')
    parser_db_connection.add_argument('--port', dest='port', type=int, help='Add mysql database port')
    args = parser_db_connection.parse_args(input.split())

    # Connect to database
    connection = connect(args.user, args.password, args.host, args.port)
    print("Connected to database server")
    return connection

def create_recovery_database(text, connection: mysql.MySQLConnection):
    # Get arguments
    input = text.split("create ")[1]

    # Parse arguments
    parser_db_connection = argparse.ArgumentParser()
    parser_db_connection.add_argument('--db-name', dest='db_name', type=str, help='Add mysql database name')
    parser_db_connection.add_argument('--schema-from', dest='schema_from', type=str, help='Add mysql database schema to recover from')
    args = parser_db_connection.parse_args(input.split())

    # Create database
    connection.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {args.db_name}")
    print("Database created!")

    # Retrieving schema from the broken database
    schema = get_schema(connection, args.schema_from)
    broken_db = args.schema_from
    recovery_db = args.db_name

    # Execute schema
    connection.cursor().execute(f"USE {args.db_name}")
    execute_schema(connection, schema)

    for entity in entities:
        connection.cursor().execute(f"ALTER TABLE {entity} ADD COLUMN (origin_id INT)")
    return [broken_db, recovery_db]

def get_schema(connection: mysql.MySQLConnection, db_name):
    print("Retrieving schema...")

    # Get tables
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SHOW TABLES FROM {db_name}")
    tables = cursor.fetchall()

    schema = ""
    for table in tables:
        table_name = table[0]
        entities.append(table_name)
        cursor.execute(f"SHOW CREATE TABLE {db_name}.{table_name}")
        create_table_stmt = cursor.fetchone()[1]
        schema += create_table_stmt + ";\n"
    print("Schema retrieved!")
    return schema

def execute_schema(connection: mysql.MySQLConnection, schema):
    print("Executing schema...")
    cursor = connection.cursor(buffered=True)
    for statement in schema.split(";\n"):
        if statement.strip():
            cursor.execute(statement)
    print("Schema executed!")

def connect(user, passwd, host, port):
    return mysql.connect(
        user=user, 
        passwd=passwd, 
        host=host, 
        port=port
    )

def copy_entry(connection: mysql.CMySQLConnection, text: str, from_db, to_db):
    input: str = text.split("copy ")[1]
    id = input.split()[0]

    parser_db_connection = argparse.ArgumentParser()
    parser_db_connection.add_argument('--only', dest='only', type=str, default="default", help='Add mysql database name')
    parser_db_connection.add_argument('--include-posts', dest='include_posts', type=str, default="default", help='Add mysql table name')
    args = parser_db_connection.parse_known_args(input.split()[1:])[0]


    cursor = connection.cursor(buffered=True)

    
    cursor.execute(f"SELECT * FROM {from_db}.feeds WHERE id = {id}")
    entry = cursor.fetchone()
    cursor.execute(f"INSERT INTO {to_db}.feeds (origin_id, name) VALUES {entry}")
    feed_id = cursor.lastrowid
    connection.commit()

    limit = f"LIMIT {args.include_posts}" if args.include_posts != "default" else ""

    query = f"SELECT * FROM {from_db}.posts WHERE feed_id = {id} {limit}"

    cursor.execute(query)
    entry = cursor.fetchall()
    # chnages the first elements of the list of tuple to the new feed_id
    entry = [(feed_id,) + e[1:] for e in entry]
    cursor.executemany(f"INSERT INTO {to_db}.posts (feed_id, url, origin_id) VALUES (%s, %s, %s)", entry)
    connection.commit()

    if (args.only != "default"):
        cursor.execute(f"SELECT * FROM {from_db}.{args.only}_sources WHERE feed_id = {id} {limit}")
        entry = cursor.fetchall()
        # chnages the first element of the tuple to the new feed_id
        entry = [(feed_id,) + e[1:] for e in entry]
        cursor.executemany(f"INSERT INTO {to_db}.{args.only}_sources (feed_id, name, fan_count, origin_id) VALUES (%s, %s, %s, %s)", entry)
        connection.commit()

    else:
        cursor.execute(f"SELECT * FROM {from_db}.instagram_sources WHERE feed_id = {id}")
        entry = cursor.fetchall()
        # chnages the first element of the tuple to the new feed_id
        entry = [(feed_id,) + e[1:] for e in entry]
        cursor.executemany(f"INSERT INTO {to_db}.instagram_sources (feed_id, name, fan_count, origin_id) VALUES (%s, %s, %s, %s)", entry)
        connection.commit()

        cursor.execute(f"SELECT * FROM {from_db}.tiktok_sources WHERE feed_id = {id}")
        entry = cursor.fetchall()
        # chnages the first element of the tuple to the new feed_id
        entry = [(feed_id,) + e[1:] for e in entry]
        cursor.executemany(f"INSERT INTO {to_db}.tiktok_sources (feed_id, name, fan_count, origin_id) VALUES (%s, %s, %s, %s)", entry)
        connection.commit()

    print("Entry copied successfully!")
    return connection

connection = None
broken_db = None
recovery_db = None
entities = []

if __name__ == '__main__':
    while True:
        text = input("> ").strip()
        command = text.split(" ")[0]
        if command == "exit":
            break
        elif command == "connect":
            connection = create_connection(text)
        elif command == "create" and connection is not None:
            [broken_db, recovery_db] = create_recovery_database(text, connection)
        elif command == "copy" and connection is not None:
            copy_entry(connection, text, broken_db, recovery_db)
