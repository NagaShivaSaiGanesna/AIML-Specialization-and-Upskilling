from concurrent.futures import ProcessPoolExecutor
import time

def calculate_square(number):
    time.sleep(2)  # Simulates a heavy computational load
    return f"Square of {number}: {number * number}"

def main():
    numbers = [1, 2, 3, 4, 5, 11, 12, 14]
    
    # Utilizing multiple CPU cores
    with ProcessPoolExecutor(max_workers=3) as executor:
        results = executor.map(calculate_square, numbers)
        
    for result in results:
        print(result,flush=True)

if __name__ == "__main__":
    main()


