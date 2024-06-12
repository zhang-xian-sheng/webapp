#!/usr/bin/env python3
# --*-- coding: utf-8 --*--

# Review 1

def add_to_list(value, my_list=None):
    """
    List is mutable, function arguments are set only once when defined.
    If the list is set to the default value, data in the list will be overwritten when used.
    """
    my_list = [] if my_list is None else my_list
    if isinstance(my_list, list):
        my_list.append(value)
    else:
        raise Exception("my_list is not None and type is not list")
    return my_list


# Review 2

def format_greeting(name, age):
    """The string is not formatted. You need to add f before it or .format(name=name, age=age) after it
    """
    return f"Hello, my name is {name} and I am {age} years old."


# Review 3

class Counter:
    count = 0
    """
    when you create an instance, self.count is initialized each time
    """
    def __init__(self):
        Counter.count += 1
        self.count = Counter.count

    def get_count(self):
        return self.count


# Review 4

import threading


class SafeCounter:
    """
    shared data is not locked, result make data errors
    """
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1


def worker(counter):
    for _ in range(1000):
        counter.increment()


counter = SafeCounter()

threads = []

for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()


# Review 5

def count_occurrences(lst):
    """
    this calculation need use += ,not =+
    """
    counts = {}

    for item in lst:

        if item in counts:

            counts[item] += 1

        else:

            counts[item] = 1

    return counts

