


class FunctionVector:
    def __init__(self, function):
        self.function = function
    
    def __call__(self, x):
        return self.function(x)
    
    def __add__(self, other):
        return FunctionVector(
            lambda x:
                self(x) + other(x)
        )
    
    def __neg__(self):
        return FunctionVector(
            lambda x:
                -self(x)
        )
    
    def __rmul__(self, scalar):
        return FunctionVector(
            lambda x:
                scalar * self(x)
        )