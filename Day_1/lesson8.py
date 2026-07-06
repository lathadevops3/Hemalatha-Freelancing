n = int(input("Enter number of Fibonacci terms: "))
a, b = 0, 1
print("Fibonacci series:")
for _ in range(n):
    print(a)
    a, b = b, a + b
