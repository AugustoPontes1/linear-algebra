

class SubspaceRules:
    @staticmethod
    def contains_zero(subspace):
        zero = subspace.parent_space.zero()
        
        return subspace.contains(zero)

    @staticmethod
    def closed_under_sum(subspace, u, v):
        if not(
            subspace.contains(u)
        ):
            return False
        
        return subspace.contains(u + v)
    
    @staticmethod
    def closed_under_scalar(subspace, scalar, u):
        if not subspace.contains(u):
            return False
        
        return subspace.contains * u