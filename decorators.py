def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function call.", args, kwargs)
        func(*args, **kwargs)
        print("After the function call.")
    return wrapper

@my_decorator
def greeting(msg, **kwargs):
    print(f"Hello, {msg}!")

greeting("FMI", test_arg="Hello")
