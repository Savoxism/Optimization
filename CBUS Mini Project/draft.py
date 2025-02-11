import numpy as np

def linear_regression(x, y):
    A = np.array([[xi, 1] for xi in x])
    
    y = np.array(y)
    
    A_T = A.T
    
    A_TA = np.dot(A_T, A) 
    
    A_TA_inv = np.linalg.inv(A_TA)
    
    A_Ty = np.dot(A_T, y)
    
    coefficients = np.dot(A_TA_inv, A_Ty)
    
    a, b = coefficients[0], coefficients[1]
    
    return a, b

x = [2, 3, 5]
y = [10, 70, 40]

a, b = linear_regression(x, y)
print(f"Coefficient a (slope): {a}")
print(f"Coefficient b (intercept): {b}")
    
    
    
    
    
    
    
    
    