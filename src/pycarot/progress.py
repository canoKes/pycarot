import math
from typing import Any, Callable

from colorama import Fore, Style


class ProgressBar:
    __slots__ = ("value", "total", "elements", "title", "digits", "percentage")

    MAX_SIZE = 50

    def __init__(
        self,
        elements: int,
        title: str = None,
        action: Callable[..., Any] = None,
        percentage: bool = True,
    ) -> None:
        self.value = 0
        self.total = elements
        self.elements = None
        if not isinstance(elements, int):
            self.total = len(elements)
            self.elements = elements

        self.title = title
        if self.title is None:
            self.title = "Progress"

        self.digits = len(str(self.total))
        self.percentage = percentage
        print(f"  {self.title}")

        if action is not None:
            self._run(action)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if value is not None:
            self._increment(True)
            print()

    def _run(self, action: Callable[..., Any]) -> None:
        collection = range(self.total)
        if self.elements is not None:
            collection = self.elements

        for x in collection:
            action(x)
            self._increment()

    def increment(self) -> None:
        self._increment()

    def _increment(self, cancel: bool = False) -> None:
        self.value += 1
        color = ""
        if cancel:
            self.value -= 1
            color = f"{Fore.RED}"
        elif self.value == self.total:
            self.value = self.total
            color = f"{Fore.GREEN}"

        scale = ProgressBar.MAX_SIZE / self.total
        progress = scale * self.value

        full_blocks = math.floor(progress)
        subs = int((progress - math.floor(progress)) * 8)
        sub_block = chr(0x2590 - subs)
        if subs == 0:
            sub_block = " "
            if self.value == self.total:
                sub_block = ""

        text = f"  {color}{chr(0x2588) * full_blocks}{sub_block}{' ' * (ProgressBar.MAX_SIZE - full_blocks - 1)}{chr(0x258F)}"
        if self.percentage:
            text += f"{int(self.value * 100 / self.total) :>3} %{Style.RESET_ALL}"
        else:
            text += f"{str.rjust(str(self.value), self.digits)}/{self.total}{Style.RESET_ALL}"

        print(text, end="\r")

        if self.total == self.value:
            print()


# for i in range(1, 11):
#     print(f"{i=}, ", end="")
#     full_blocks = i // 8
#     print(f"{full_blocks=}, ", end="")
#     sub_block = i % 8
#     if sub_block == 0:
#         sub_block = 8
#     # sub_block = 8 if sub_block == 0 else sub_block
#     print(f"{sub_block=}, ", end="")
#     print(chr(0x2590 - sub_block))
