# Parallel Computing for CPU-Bound Tasks: High-Performance Factorial Calculation

In high-performance computing, some tasks are purely limited by the speed of the processor. These are known as **CPU-bound tasks**. Calculating factorials for extremely large numbers is a perfect example of such a workload. This guide explores how to use Python's **Multiprocessing** module to distribute these heavy mathematical computations across multiple CPU cores.

---

## 1. Understanding CPU-Bound Workloads

When a program performs complex mathematical operations, it relies heavily on the CPU. In a standard sequential program, only one CPU core is utilized, while the others remain idle.

### The Problem with Single-Core Execution

If you calculate the factorials of several large numbers (like 5,000 or 10,000) one after another, the total time is the sum of each calculation. This is inefficient because modern computers have multiple cores that could be working simultaneously.

### The Multiprocessing Solution

By creating a **Pool** of processes, we can assign different numbers to different CPU cores. Instead of one core doing all the work, four, eight, or even thirty-two cores can share the load, significantly reducing the total execution time.

---

## 2. Overcoming Python's Integer Limits

Python has a built-in safety limit for the number of digits allowed when converting integers to strings to prevent potential Denial of Service (DoS) attacks via very large numbers.

To work with factorials of numbers like 5,000+, we must manually increase this limit using the `sys` module.

```python
import sys

# Increase the limit for integer string conversion to 100,000 digits
sys.set_int_max_str_digits(100000)

```

---

## 3. Implementation: Parallel Factorial Calculation

The following implementation uses `multiprocessing.Pool` to map a list of numbers to a factorial function across all available CPU cores.

### The Factorial Function

```python
import multiprocessing
import math
import time
import sys

# Essential for large number handling
sys.set_int_max_str_digits(100000)

def compute_factorial(n):
    """Computes the factorial of a large number."""
    print(f"Computing factorial for {n}...")
    result = math.factorial(n)
    return result

```

### The Main Execution Logic

The `multiprocessing.Pool` object automatically detects the number of cores in your machine and creates that many worker processes.

```python
if __name__ == "__main__":
    numbers = [5000, 6000, 7000, 8000]
    
    start_time = time.time()

    # Create a pool of worker processes
    with multiprocessing.Pool() as pool:
        # map() distributes the 'numbers' list across the 'compute_factorial' function
        results = pool.map(compute_factorial, numbers)

    end_time = time.time()
    
    print(f"Time taken: {end_time - start_time:.4f} seconds")

```

---

## 4. Key Performance Insights

### Why use `multiprocessing.Pool`?

* **Automatic Distribution:** You don't need to manually create each process; the `Pool` handles the distribution of the list items.
* **Efficiency:** It keeps all your CPU cores busy. If one core finishes its factorial calculation early, the pool immediately assigns it the next number from the list.
* **Speed:** In the example provided, calculating multiple large factorials took only a few seconds. In a single-threaded approach, this could take significantly longer and might even cause the system to become unresponsive.

### Comparison: Single-core vs. Multi-core

| Feature | Single-threaded (Sequential) | Multiprocessing (Parallel) |
| --- | --- | --- |
| **CPU Usage** | Only 1 core used | All available cores used |
| **Execution Time** |  |  Time of the longest single task |
| **System Stability** | High risk of "hanging" on heavy tasks | Better stability via load distribution |

---

## 5. Conclusion

Multiprocessing is a game-changer for data science, engineering, and mathematical applications in Python. By bypassing the Global Interpreter Lock (GIL) and utilizing the full power of your hardware, you can transform computationally expensive tasks into efficient, high-speed operations.

Would you like me to help you create a **GitHub README** or a **Jupyter Notebook** structure for this multiprocessing project?