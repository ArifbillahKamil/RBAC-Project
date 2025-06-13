import mysql.connector
import threading
import time
import statistics

# Konfigurasi koneksi MySQL
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'db_sistem_restore',
    'port': 3306,
    'connection_timeout': 10
}

# Query yang ingin dites
QUERY = "SELECT * FROM mahasiswa LIMIT 1000;"  # Silakan ganti dengan query yang mau dites

# Konfigurasi stress test
NUM_THREADS = 10      # jumlah koneksi concurrent (simulasi user)
ITERATIONS = 20       # berapa kali masing-masing thread menjalankan query

# Untuk hasil waktu eksekusi
execution_times = []
result_counts = []  # menampung jumlah row hasil query
errors = 0
lock = threading.Lock()

def run_query():
    global errors
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for _ in range(ITERATIONS):
            start_time = time.time()
            try:
                cursor.execute(QUERY)
                results = cursor.fetchall()
                elapsed = time.time() - start_time
                with lock:
                    execution_times.append(elapsed)
                    result_counts.append(len(results))
            except Exception as e:
                with lock:
                    errors += 1
                print(f"Query error: {e}")

        cursor.close()
        conn.close()

    except Exception as e:
        with lock:
            errors += 1
        print(f"Connection error: {e}")

if __name__ == "__main__":
    print("Memulai stress test...")
    threads = []
    start_test = time.time()

    for _ in range(NUM_THREADS):
        t = threading.Thread(target=run_query)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_test = time.time() - start_test

    print("\n===== Hasil Stress Test =====")
    print(f"Total waktu: {total_test:.2f} detik")
    print(f"Total query: {NUM_THREADS * ITERATIONS}")
    print(f"Total error: {errors}")
    if execution_times:
        print(f"Rata-rata waktu eksekusi: {statistics.mean(execution_times):.4f} detik")
        print(f"Min waktu eksekusi: {min(execution_times):.4f} detik")
        print(f"Max waktu eksekusi: {max(execution_times):.4f} detik")
    if result_counts:
        print(f"Jumlah rata-rata hasil query per eksekusi: {statistics.mean(result_counts):.0f} rows")
