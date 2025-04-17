import numpy as np

def check_grad(fn, gr, X):
    X_flat = X.reshape(-1) # convert X to an 1D array -> 1 for loop needed
    shape_X = X.shape
    num_grad = np.zeros_like(X)
    grad_flat = np.zeros_like(X_flat)
    eps = 1e-6
    numElems = X_flat.shape[0]
    
    # calculate numerical gradient
    for i in range(numElems):
        Xp_flat = X_flat.copy()
        Xn_flat = X_flat.copy()
        Xp_flat[i] += eps
        Xn_flat[i] -= eps
        Xp = Xp_flat.reshape(shape_X)
        Xn = Xn_flat.reshape(shape_X)
        grad_flat[i] = (fn(Xp) - fn(Xn)) / (2 * eps)
        
    num_grad = grad_flat.reshape(shape_X)
    
    diff = np.linalg.norm(num_grad - gr(X))
    print(diff)
    
m, n = 10, 20
A = np.random.randn(m, n)
X = np.random.randn(n, m)

def fn1(X):
    return np.trace(A.dot(X))

def gr1(X):
    return A.T

check_grad(fn1, gr1, X)

