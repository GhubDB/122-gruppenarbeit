import os
import shutil
import schedule
import threading
import time


def backup_database():
    timestamp = time.strftime("%H_%M_%S_%d_%m_%Y")
    filename = f"database_backup_{timestamp}.sqlite3"

    print("Current Working Directory:", os.getcwd())

    try:
        shutil.copy("workulator_database.sqlite3", filename)
        result = f"Backup successful: {filename}"

    except Exception as e:
        result = f"Backup failed: {str(e)}"

    print(result)


def schedule_backup():
    schedule.every().day.at("09:00").do(backup_database)
    schedule.every().day.at("16:00").do(backup_database)


def start_backup_scheduler():
    # Start the scheduling in a separate thread
    scheduler_thread = threading.Thread(target=schedule_backup)
    scheduler_thread.start()


if __name__ == "__main__":
    backup_database()
