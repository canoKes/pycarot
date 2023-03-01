import unittest

from pycarot import event


class TestEvent(unittest.TestCase):
    def test_subscribe(self) -> None:
        manager = event.EventManager()
        manager.subscribe(self)
        for sub in manager._subs.values():
            if sub == self:
                self.assertTrue(True)
                return
        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
