
import sqlite3


def create_database():

    connection = sqlite3.connect("monitoring_data.db")
    cursor = connection.cursor()

    # Create monitoring history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT,
            ip_address TEXT,
            status TEXT,
            latency REAL,
            timestamp TEXT,
            packets_sent INTEGER,
            packets_received INTEGER,
            packet_loss REAL
        )
    """)

    # Add new columns to an existing database if needed
    cursor.execute("PRAGMA table_info(monitoring_history)")
    existing_columns = [column[1] for column in cursor.fetchall()]

    new_columns = {
        "packets_sent": "INTEGER",
        "packets_received": "INTEGER",
        "packet_loss": "REAL"
    }

    for column, data_type in new_columns.items():
        if column not in existing_columns:
            cursor.execute(
                f"ALTER TABLE monitoring_history ADD COLUMN {column} {data_type}"
            )

    # Create alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT,
            ip_address TEXT,
            alert_type TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_record(name, ip, status, latency, timestamp,
                packets_sent=None, packets_received=None, packet_loss=None):

    connection = sqlite3.connect("monitoring_data.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO monitoring_history
        (device_name, ip_address, status, latency, timestamp,
         packets_sent, packets_received, packet_loss)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, ip, status, latency, timestamp,
        packets_sent, packets_received, packet_loss
    ))

    connection.commit()
    connection.close()


# Save network fault alerts
def save_alert(name, ip, alert_type, message, timestamp):

    connection = sqlite3.connect("monitoring_data.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO alerts
        (device_name, ip_address, alert_type, message, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name, ip, alert_type, message, timestamp
    ))

    connection.commit()
    connection.close()


