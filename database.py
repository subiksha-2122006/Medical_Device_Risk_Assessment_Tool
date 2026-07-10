import sqlite3
print("DATABASE FILE LOADED")
print("DATABASE FILE LOADED - NEW VERSION")
DB_NAME = "risk_management.db"


# -------------------------
# DATABASE CONNECTION
# -------------------------

def get_connection():
    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )


# -------------------------
# CREATE TABLES
# -------------------------

def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # USERS TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # HAZARDS TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hazards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hazard_name TEXT,
        severity INTEGER,
        probability INTEGER,
        risk_score INTEGER,
        risk_level TEXT,
        mitigation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # FMEA TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fmea (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        failure_mode TEXT,
        effect TEXT,
        cause TEXT,
        severity INTEGER,
        occurrence INTEGER,
        detection INTEGER,
        rpn INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # AUDIT LOG TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        action TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# ADD HAZARD
# -------------------------

def add_hazard(
    hazard_name,
    severity,
    probability,
    risk_score,
    risk_level,
    mitigation
):
    print("ADD_HAZARD CALLED")

    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO hazards
        (
            hazard_name,
            severity,
            probability,
            risk_score,
            risk_level,
            mitigation
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            hazard_name,
            severity,
            probability,
            risk_score,
            risk_level,
            mitigation
        ))

        conn.commit()

        print("HAZARD SAVED SUCCESSFULLY")

    except Exception as e:
        print("ERROR INSIDE ADD_HAZARD:")
        print(e)
        raise

    finally:
        conn.close()

# -------------------------
# GET ALL HAZARDS
# -------------------------

def get_all_hazards():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM hazards
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# -------------------------
# DELETE HAZARD
# -------------------------

def delete_hazard(hazard_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM hazards
    WHERE id = ?
    """, (hazard_id,))

    conn.commit()

    conn.close()


# -------------------------
# ADD AUDIT ENTRY
# -------------------------

def add_audit_log(
    username,
    action
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO audit_log
    (
        username,
        action
    )
    VALUES (?, ?)
    """,
    (
        username,
        action
    ))

    conn.commit()

    conn.close()


# -------------------------
# GET AUDIT LOGS
# -------------------------

def get_audit_logs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM audit_log
    ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    conn.close()

    return logs
# -------------------------
# ADD FMEA RECORD
# -------------------------

def add_fmea(
    failure_mode,
    effect,
    cause,
    severity,
    occurrence,
    detection,
    rpn
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO fmea
    (
        failure_mode,
        effect,
        cause,
        severity,
        occurrence,
        detection,
        rpn
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        failure_mode,
        effect,
        cause,
        severity,
        occurrence,
        detection,
        rpn
    ))

    conn.commit()
    conn.close()
# -------------------------
# GET ALL FMEA RECORDS
# -------------------------

def get_all_fmea():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM fmea
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data
