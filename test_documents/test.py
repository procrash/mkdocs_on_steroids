# Test Python file for document upload service 
 
def fibonacci(n): 
    """Calculate the nth Fibonacci number.""" 
    if n <= 1: 
        return n 
    return fibonacci(n-1) + fibonacci(n-2) 
 
class Calculator: 
    """A simple calculator class.""" 
    def add(self, a, b): 
        return a + b 
 
if __name__ == "__main__": 
    print(fibonacci(10)) 
