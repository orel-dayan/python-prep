# List comprehensions, generators
squares = [x**2 for x in range(10) if x % 2 == 0]
gen = (x**2 for x in range(10))  # lazy — יודעת את ההבדל?

# Decorators
def retry(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    pass
        return wrapper
    return decorator

# Context managers
with open("file.txt") as f:  # יודעת לממש __enter__/__exit__?
    data = f.read()