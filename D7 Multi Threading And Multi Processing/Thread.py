import threading
import time

def download_file(file_name):
    print(f"Starting download: {file_name}...")
    time.sleep(2)  # Simulating a 2-second network delay
    print(f"Finished download: {file_name}")

# Without Threading (Sequential)
start = time.perf_counter()
download_file("Data_1.csv")
download_file("Data_2.csv")
end = time.perf_counter()
print(f"Sequential time: {round(end - start, 2)} seconds\n")

# With Multithreading
start = time.perf_counter()
t1 = threading.Thread(target=download_file, args=("Data_1.csv",))
t2 = threading.Thread(target=download_file, args=("Data_2.csv",))

t1.start()
t2.start()

t1.join() # Wait for t1 to finish
t2.join() # Wait for t2 to finish
end = time.perf_counter()
print(f"Multithreaded time: {round(end - start, 2)} seconds")