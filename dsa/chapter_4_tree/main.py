import numpy as np
import matplotlib.pyplot as plt

class LinearRegression:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = None
        
    def fit(self, X, y):
        """
        Train the linear regression model using gradient descent.
        
        Parameters:
        X: Training features
        y: Target values
        """
        # Initialize parameters
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        # Ensure y is a 1D array to avoid broadcasting issues
        y = y.reshape(-1)
        
        # Gradient descent
        for _ in range(self.iterations):
            y_predicted = np.dot(X, self.weights) + self.bias
            
            dw = (1/n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1/n_samples) * np.sum(y_predicted - y)
            
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
            
    def predict(self, X):
        """
        Make predictions with trained model.
        
        Parameters:
        X: Features to predict on
        
        Returns:
        y_pred: Predicted values
        """
        return np.dot(X, self.weights) + self.bias
    
    def fit_normal_equation(self, X, y):
        """
        Train using the normal equation (closed-form solution).
        """
        # Ensure y is properly shaped
        y = y.reshape(-1)
        
        X_b = np.c_[np.ones((X.shape[0], 1)), X]  # Add intercept term
        theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
        self.bias = theta[0]
        self.weights = theta[1:]

# Example usage:
if __name__ == "__main__":
    # Generate some sample data
    np.random.seed(42)
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)
    
    # Fit model using gradient descent
    model_gd = LinearRegression(learning_rate=0.1, iterations=1000)
    model_gd.fit(X, y)
    
    # Fit model using normal equation
    model_ne = LinearRegression()
    model_ne.fit_normal_equation(X, y)
    
    # Print results
    print("Gradient Descent - Weights:", model_gd.weights, "Bias:", model_gd.bias)
    print("Normal Equation - Weights:", model_ne.weights, "Bias:", model_ne.bias)
    
    # Plot results
    plt.scatter(X, y)
    x_range = np.array([[0], [2]])
    plt.plot(x_range, model_gd.bias + model_gd.weights * x_range, 'r', label='Gradient Descent')
    plt.plot(x_range, model_ne.bias + model_ne.weights * x_range, 'g', label='Normal Equation')
    plt.xlabel('X')
    plt.ylabel('y')
    plt.legend()
    plt.show()