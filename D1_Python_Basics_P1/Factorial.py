def get_factorial(n: int) -> int:
    """
    Calculates the factorial of a non-negative integer using recursion.

    Args:
        n (int): The number to calculate the factorial of.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is negative.
        RecursionError: If n is too large for the stack.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    
    # Base case
    if n == 0:
        return 1
    
    return n * get_factorial(n - 1)

def main():
    try:
        user_input = input("Enter a non-negative integer: ")
        # Input validation
        val = int(user_input)
        print(f"The factorial is: {get_factorial(val)}")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except RecursionError:
        print("Value too large to calculate with recursion.")

if __name__ == "__main__":
    main()