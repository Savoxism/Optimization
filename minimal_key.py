def closure(attributes, fds):
    """
    Compute the closure of 'attributes' under functional dependencies 'fds'.
    - attributes: iterable of attribute names (e.g. ['A','B'])
    - fds: list of tuples (lhs, rhs), where lhs and rhs are iterables of attribute names
    """
    closure_set = set(attributes)

    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if set(lhs).issubset(closure_set) and not set(rhs).issubset(closure_set):
                closure_set.update(rhs)
                changed = True
    return closure_set

def minimal_key_method1(U, fds):
    """
    Method 1: Iterative-removal starting from the full attribute set U.
    Returns one minimal key.
    """
    K = set(U)

    for attr in list(U):
        candidate = K - {attr}
        if closure(candidate, fds) == set(U):
            K = candidate
    return K

def minimal_key_method2(U, fds):
    VT = set().union(*(lhs for lhs, _ in fds))

    VP = set().union(*(rhs for _, rhs in fds))

    # X = attributes that must be in the key
    X = set(U) - VP

    # Y = attributes that MUST NOT be in the key
    # Y = VP - VT

    # Z = attributes that MAY or MAY NOT be in the key
    Z = VP & VT


    if closure(X, fds) == set(U):
        return X
    
    K = set(X) | set(Z)

    for a in list(Z):
        candidate = K - {a}
        if closure(candidate, fds) == set(U):
            K.remove(a)
        
    return K

schemas = [
    ("Schema1", 
     ['A','B','C','D','E'], 
     [
         (('A',),   ('B',)),
         (('A',),   ('C',)),
         (('B',),   ('D',)),
         (('C','D'),('E',)),
         (('E',),   ('A',))
     ]
    ),
]

for name, U, fds in schemas:
    key1 = minimal_key_method1(U, fds)
    key2 = minimal_key_method2(U, fds)
    print(f"{name}:")
    print("  Method 1 minimal key:", key1)
    print("  Method 2 minimal key:", key2)
    print()