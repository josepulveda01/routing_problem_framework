import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
        port=int(os.getenv("MYSQL_PORT", 3306))
    )


def init_db(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instances (
            instance_id INT AUTO_INCREMENT PRIMARY KEY,
            n_nodes INT NOT NULL,
            seed INT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id INT AUTO_INCREMENT PRIMARY KEY,
            instance_id INT NOT NULL,
            solver VARCHAR(50) NOT NULL,
            seed INT NOT NULL,
            cost DOUBLE NOT NULL,
            time_ms DOUBLE NOT NULL,
            route TEXT NOT NULL,
            FOREIGN KEY (instance_id) REFERENCES instances(instance_id)
        )
    """)

    conn.commit()


def insert_instance(conn, n, seed):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO instances (n_nodes, seed) VALUES (%s, %s)",
        (n, seed)
    )
    conn.commit()
    return cursor.lastrowid


def insert_run(conn, instance_id, solver, seed, cost, time_ms, route):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO runs (
            instance_id, solver, seed, cost, time_ms, route
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (instance_id, solver, seed, cost, time_ms, str(route))
    )
    conn.commit()
