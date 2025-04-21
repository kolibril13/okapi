# Function to calculate Fibonacci numbers
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Print the first 100 Fibonacci numbers
for i in range(1, 101):
    fib_number = fibonacci(i)
    print(f"Fibonacci number {i} is: {fib_number}")