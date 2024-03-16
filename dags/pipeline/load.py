import psycopg2
from psycopg2 import sql
import config.config as sc

user, host, password = sc.get_postgres_creds()


def write_data_to_tables(data):
    con = get_pg_connecter()
    check_tables_exists(con)
    try:
        cur = con.cursor()
        for row in data:
            query = build_query(row)
            cur.execute(query)
        cur.close()
        con.close()
    except:
        con.close()


def build_query(row: dict):
    col_names = sql.SQL(", ").join(sql.Identifier(col) for col in row.keys())
    values = [val for val in row.values()]
    values = sql.SQL(" , ").join(sql.Literal(val) for val in values)
    query = sql.SQL(
        """
        INSERT INTO staging ({col_names}) VALUES ({values})
        ON CONFLICT (uri, country) DO UPDATE
        SET date_added = {date}
        """
    ).format(col_names=col_names, values=values, date=sql.Literal(row["date_added"]))

    return query


def get_pg_connecter() -> psycopg2.extensions.connection:
    try:
        con = psycopg2.connect(
            f"dbname='spotify' user='{user}' host='{host}' password='{password}'"
        )
        con.autocommit = True
        print("Database Exists.")
        return con

    except psycopg2.OperationalError as Error:
        con = psycopg2.connect(f"user='{user}' host='{host}' password='{password}'")
        con.autocommit = True
        cur = con.cursor()
        cur.execute(
            sql.SQL("CREATE DATABASE spotify;").format(sql.Identifier("spotify"))
        )
        con.close()
        return psycopg2.connect(
            f"dbname='spotify' user='{user}' host='{host}' password='{password}'"
        )


def check_tables_exists(con):
    cur = con.cursor()
    command = """
        CREATE TABLE IF NOT EXISTS staging (
            id bigserial,
            date_added timestamp,
            uri text,
            track_href text,
            name text,
            artist text,
            country text,
            type text,
            tempo real,
            duration_ms int,
            time_signature int,
            key int,
            mode int,
            danceability real,
            energy real,
            loudness real,
            liveness real,
            valence real,
            speechiness real,
            acousticness real,
            instrumentalness real,
            unique (uri, country)
            )
        """
    cur.execute(command)
