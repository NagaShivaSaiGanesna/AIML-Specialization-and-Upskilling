import multiprocessing
import time

def square_numbers():
    for i in range(5):
        time.sleep(1) 
        # flush=True forces the output to the console immediately
        print(f"Square: {i * i}", flush=True)

def cube_numbers():
    for i in range(5):
        time.sleep(1.5) 
        print(f"Cube: {i * i * i}", flush=True)

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=square_numbers)
    p2 = multiprocessing.Process(target=cube_numbers)

    p1.start()
    p2.start()

    p1.join()
    p2.join()