import numpy as np

a = np.zeros(10, int)

for i in range(1, 10):
    print("insert: ", i)
    a[i] = i

print(type(a))  # Prints "<class 'numpy.ndarray'>"
print(a.shape)  # Prints "(3,)"
print(a[0], a[1], a[2])  # Prints "1 2 3"
print(a)  # Prints "[5, 2, 3]"

print("Sum: ", a.sum())
print("Cumulative Sum: ", a.cumsum())
print("Mean: ", a.mean())
print("Median: ", np.median(a))
print("StdDev: ", a.std())
print("Size: ", a.size)

b = np.array([[1, 2, 3], [4, 5, 6]])  # Create a rank 2 array
print(b.shape)  # Prints "(2, 3)"
print(b[0, 0], b[0, 1], b[1, 0])  # Prints "1 2 4"

print("hello world d")