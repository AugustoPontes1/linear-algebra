from dataclasses import dataclass

from sim.calculations.vector import Vector


@dataclass
class RuleResult:
    name: str
    valid: bool
    left: object = None
    right: object = None
    explanation: str = ""

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


class VectorSpaceAxioms:
    @staticmethod
    def check_all(
        operations,
        u,
        v,
        w,
        a,
        b
    ):
        add = operations.add
        smul = operations.scalar_mul
        
        results = []
        
        # 1. Association
        left = add(
            add(u, v),
            w,
        )
        
        right = add(
            u,
            add(v, w),
        )
        
        results.append(
            RuleResult(
                "(u + v) + w = u + (v + w)",
                left == right,
                left,
                right,
            )
        )
        
        # 2. Commutativity
        left = add(u,v)
        right = add(v, u)
        
        results.append(
            RuleResult(
                "u + v = v + u",
                left == right,
                left,
                right,
            )
        )
        
        # 3. Null vector
        if operations.zero is None:
            results.append(
                RuleResult(
                    "u + 0 = u",
                    False,
                    explanation=(
                        "Nenhum neutro aditivo "
                        "foi definido."                        
                    ),
                )
            )
        else:
            zero = operations.zero
            
            left = add(
                u,
                zero,
            )
            
            results.append(
                RuleResult(
                    "u + 0 = u",
                    left == u,
                    left,
                    u,
                )
            )
        
        # 4. Oppostive vector
        if(
            operations.zero is None
            or operations.opposite is None
        ):
            results.append(
                "u + (-u) = 0",
                False,
                explanation=(
                    "Não há candidato a "
                    "oposto definido."                    
                ),
            )
        else:
            opposite = operations.opposite(u)
            
            left = add(
                u,
                opposite,
            )
            
            results.append(
                RuleResult(
                    "u + (-u) = 0",
                    left == operations.zero,
                    left,
                    operations.zero
                )
            )
        
        # 5. a(u+v)
        left = smul(
            a,
            add(u, v),
        )
        
        right = add(
            smul(a, u),
            smul(a, v),
        )
        
        results.append(
            RuleResult(
                "a(u + v) = au + av",
                left == right,
                left,
                right,
            )
        )
        
        # 6. (a+b)v
        left = smul(
            a + b,
            v,
        )
        
        right = add(
            smul(a, v),
            smul(b, v),
        )
        
        results.append(
            RuleResult(
                "(a + b)v = av + bv",
                left == right,
                left,
                right,
            )
        )
        
        # 7. (ab)v
        left = smul(
            a * b,
            v,
        )
        
        right = smul(
            a,
            smul(b, v),
        )
        
        results.append(
            RuleResult(
                "(ab)v = a(bv)",
                left == right,
                left,
                right,
            )
        )
        
        # 8. 1v
        left = smul(
            1,
            v,
        )
        
        results.append(
            RuleResult(
                "1v = v",
                left == v,
                left,
                v,
            )
        )
        
        return results