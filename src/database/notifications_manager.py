# src/database/notifications_manager.py
from src.database.db import get_connection

def add_db_notification(user_id, trip_id, icon, title, text, timestamp):
    """
    Inserts a new notification alert for the specified user and trip.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO notifications (user_id, trip_id, icon, title, text, timestamp, is_read)
            VALUES (?, ?, ?, ?, ?, ?, 0)
            """,
            (user_id, trip_id, icon, title, text, timestamp)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Error adding database notification:", e)
        return None
    finally:
        conn.close()

def get_db_notifications(user_id, trip_id=None):
    """
    Retrieves all notifications for a specific user, optionally filtered by trip_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if trip_id is not None:
            cursor.execute(
                """
                SELECT id, trip_id, icon, title, text, timestamp, is_read
                FROM notifications
                WHERE user_id = ? AND trip_id = ?
                ORDER BY id DESC
                """,
                (user_id, trip_id)
            )
        else:
            cursor.execute(
                """
                SELECT id, trip_id, icon, title, text, timestamp, is_read
                FROM notifications
                WHERE user_id = ?
                ORDER BY id DESC
                """,
                (user_id,)
            )
        rows = cursor.fetchall()
        notifications = []
        for r in rows:
            notifications.append({
                "id": r[0],
                "trip_id": r[1],
                "icon": r[2],
                "title": r[3],
                "text": r[4],
                "timestamp": r[5],
                "is_read": r[6]
            })
        return notifications
    except Exception as e:
        print("Error getting database notifications:", e)
        return []
    finally:
        conn.close()

def clear_db_notifications(user_id, trip_id=None):
    """
    Deletes all notifications for a specific user, optionally filtered by trip_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if trip_id is not None:
            cursor.execute(
                "DELETE FROM notifications WHERE user_id = ? AND trip_id = ?",
                (user_id, trip_id)
            )
        else:
            cursor.execute(
                "DELETE FROM notifications WHERE user_id = ?",
                (user_id,)
            )
        conn.commit()
        return True
    except Exception as e:
        print("Error clearing database notifications:", e)
        return False
    finally:
        conn.close()

def mark_db_notification_read(user_id, notification_id):
    """
    Marks a specific notification as read.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE notifications SET is_read = 1 WHERE user_id = ? AND id = ?",
            (user_id, notification_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error marking notification as read:", e)
        return False
    finally:
        conn.close()
