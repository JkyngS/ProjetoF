import os
import cx_Oracle
from contextlib import contextmanager
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

def _build_dsn():
    host = os.getenv("DB_HOST", "10.14.1.53")
    port = int(os.getenv("DB_PORT", "1521"))
    service = os.getenv("DB_SERVICE", "dbprod")
    sid = os.getenv("DB_SID")

    if sid:
        return cx_Oracle.makedsn(host, port, sid=sid)
    return cx_Oracle.makedsn(host, port, service_name=service)

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = cx_Oracle.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dsn=_build_dsn(),
            encoding="UTF-8"  # timeout removido porque cx_Oracle não suporta
        )
        yield conn
    finally:
        try:
            if conn:
                conn.close()
        except Exception:
            pass
