counter = 0

# def increment():
#     counter += 1      # UnboundLocalError! assignment makes it local

def increment_fixed():
    global counter    # explicit: use the module-level variable
    counter += 1

def outer():
    count = 0
    def inner():
        nonlocal count    # use the ENCLOSING function's variable
        count += 1
    inner()
    return count


def make_multiplier(factor):
    def multiply(x):
        return x * factor     # remembers 'factor' after make_multiplier returned
    return multiply

double = make_multiplier(2)
double(5)      # 10