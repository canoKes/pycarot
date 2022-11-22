import time
import numpy as np
from pycarot.progress import ProgressBar

values = np.arange(250)
delay = 0.005

######################
# Example 1
######################
with ProgressBar(values, title="Example 1") as bar:
    for _ in values:
        time.sleep(delay)
        bar.increment()


######################
# Example 2
######################
bar = ProgressBar(values, title="Example 2")
for _ in values:
    time.sleep(delay)
    bar.increment()


######################
# Example 3
######################
result = []


def first_action(value: int) -> None:
    global result
    time.sleep(delay)
    result.append(value)


with ProgressBar(values, title="Example 3", action=first_action) as _:
    pass

print(len(result))

######################
# Example 4
######################
result = []
values = [f"gnirts {i + 1}" for i in range(250)]


def second_action(value: str) -> None:
    global result
    time.sleep(delay)
    data = value.split()
    result.append(f"{data[0][::-1]} {data[1]}")


with ProgressBar(values, title="Example 4", action=second_action) as _:
    pass
[print(x) for x in result]
