
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_dashboard_data():

    connection = sqlite3.connect("monitoring_data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT device_name, ip_address, status, latency,
               timestamp, packets_sent, packets_received, packet_loss
        FROM monitoring_history
        WHERE id IN (
            SELECT MAX(id)
            FROM monitoring_history
            GROUP BY device_name
        )
    """)

    devices = cursor.fetchall()

    total = len(devices)

    online = sum(
        1 for d in devices if d["status"] == "ONLINE"
    )

    offline = total - online

    latencies = [
        d["latency"] for d in devices
        if d["latency"] is not None
    ]

    average_latency = (
        round(sum(latencies) / len(latencies), 2)
        if latencies else 0
    )

    losses = [
        d["packet_loss"] for d in devices
        if d["packet_loss"] is not None
    ]

    average_packet_loss = (
        round(sum(losses) / len(losses), 2)
        if losses else 0
    )

    # Highest latency device
    highest_latency_device = (
        max(
            [d for d in devices if d["latency"] is not None],
            key=lambda d: d["latency"],
            default=None
        )
    )

    # Highest packet loss device
    highest_loss_device = (
        max(
            [d for d in devices if d["packet_loss"] is not None],
            key=lambda d: d["packet_loss"],
            default=None
        )
    )

    # Network health score
    network_health = (
        round((online / total) * 100, 2)
        if total else 0
    )

    if network_health >= 90:
        health_status = "Excellent"
    elif network_health >= 70:
        health_status = "Good"
    else:
        health_status = "Poor"

    cursor.execute("""
        SELECT device_name, latency, packet_loss, timestamp
        FROM monitoring_history
        ORDER BY id DESC
        LIMIT 20
    """)

    history = list(reversed(cursor.fetchall()))

    chart_labels = [
        record["timestamp"].split()[-1]
        for record in history
    ]

    chart_latencies = [
        record["latency"] for record in history
    ]

    chart_packet_losses = [
        record["packet_loss"] for record in history
    ]

    cursor.execute("""
        SELECT device_name, ip_address, alert_type, message, timestamp
        FROM alerts
        ORDER BY id DESC
        LIMIT 20
    """)

    alerts = cursor.fetchall()

    connection.close()

    return (
        devices,
        total,
        online,
        offline,
        average_latency,
        average_packet_loss,
        history,
        chart_labels,
        chart_latencies,
        chart_packet_losses,
        alerts,
        highest_latency_device,
        highest_loss_device,
        network_health,
        health_status
    )


@app.route("/")
def dashboard():

    (
        devices,
        total,
        online,
        offline,
        average_latency,
        average_packet_loss,
        history,
        chart_labels,
        chart_latencies,
        chart_packet_losses,
        alerts,
        highest_latency_device,
        highest_loss_device,
        network_health,
        health_status
    ) = get_dashboard_data()

    return render_template(
        "index.html",
        devices=devices,
        total=total,
        online=online,
        offline=offline,
        average_latency=average_latency,
        average_packet_loss=average_packet_loss,
        history=history,
        chart_labels=chart_labels,
        chart_latencies=chart_latencies,
        chart_packet_losses=chart_packet_losses,
        alerts=alerts,
        highest_latency_device=highest_latency_device,
        highest_loss_device=highest_loss_device,
        network_health=network_health,
        health_status=health_status
    )


if __name__ == "__main__":
    app.run(debug=True)




