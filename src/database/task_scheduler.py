import os
import subprocess
import schedule
import threading
import time


def backup_database():
    # Generate the filename with timestamp
    timestamp = time.strftime("%H_%M_%S_%d_%m_%Y")
    filename = f"database_backup_{timestamp}.sqlite3"

    print("Current Working Directory:", os.getcwd())

    # Run the Bash script in a subprocess
    process = subprocess.Popen(
        ["bash", "src/database/backup-bash.sh", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, error = process.communicate()

    # Handle the result of the backup
    if process.returncode == 0:
        result = f"Backup successful: {output.decode('utf-8')}"
    else:
        result = f"Backup failed: {error.decode('utf-8')}"

    print(result)
    return result


def schedule_backup():
    schedule.every().day.at("09:00").do(backup_database)
    schedule.every().day.at("16:00").do(backup_database)


def start_backup_scheduler():
    # Start the scheduling in a separate thread
    scheduler_thread = threading.Thread(target=schedule_backup)
    scheduler_thread.start()


if __name__ == "__main__":
    backup_database()
