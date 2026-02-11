from concurrent.futures import ThreadPoolExecutor
import time

def print_number(number):
    time.sleep(1)  # Simulates an I/O-bound task
    return f"Processed Number: {number}"

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Max_workers defines the number of threads running concurrently
with ThreadPoolExecutor(max_workers=3) as executor:
    # .map() applies the function to every item in the list across the threads
    results = executor.map(print_number, numbers)

for result in results:
    print(result)