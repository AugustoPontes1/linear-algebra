from vector import Vector

class VectorSpaceRules:
    
    @staticmethod
    def associative_sum(u, v, w):
        left = (u + v) + w
        right = u + (v + w)
        
        return left, right, left == right

    @staticmethod
    def distributive_vector(a, u, v):
        return a * (u + v) == (a * u) + (a * v)
    
    @staticmethod
    def commutative_sum(u, v):
        left = u + v
        right = v + u
        
        return left, right, left == right

    @staticmethod
    def null_vector(u):
        zero = Vector([0] * len(u.values))
        
        left = u + zero
        right = u
        
        return left, right, left == right

    @staticmethod
    def opposite_vector(u):
        zero = Vector([0] * len(u.values))
        
        left = u + (-u)
        right = zero
        
        return left, right, left == right

    @staticmethod
    def closure_sum(space, u, v):
        if not space.contains(u) or not space.contains(v):
            return False
        
        result = u + v
        
        return space.contains(result)
    
    @staticmethod
    def closure_scalar(space, a, u):
        if not isinstance(a, (int, float)):
            return False
        
        if not space.contains(u):
            return False
        
        result = a * u
        
        return space.contains(result)
    
    @staticmethod
    def distributive_scalars(a, b, v):
        return (a + b) * v == (a * v) + (b * v)
    
    @staticmethod
    def associative_scalars(a, b, v):
        return (a * b) * v == a * (b * v)
    
    @staticmethod
    def scalar_identity(v):
        return 1 * v == v