a = 10.5
if isinstance(a, (int, float)):
    print("This is a number!")

print(5 or 0)

import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])
subset = arr[:,:]
subset[:,1] = 0
print(subset)
