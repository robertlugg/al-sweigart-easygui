import unittest
import sys
import os
import time
import threading

try:
    import pyautogui # PyAutoGUI simulates key presses on the message boxes.
except:
    sys.exit('The unit tests for easygui require the PyAutoGUI module. Use pip to install pyautogui from PyPI.')
pyautogui.PAUSE = 0.1

sys.path.insert(0, os.path.abspath('..'))
import easygui

GUI_WAIT = 0.2 # if tests start failing, maybe try bumping this up a bit (though that'll slow the tests down)

runningOnPython2 = sys.version_info[0] == 2


# TODO - test the image displaying capabilities when PyAutoGUI supports screenshot recognition.


class KeyPresses(threading.Thread):
    def __init__(self, keyPresses, interval=0.05):
        super(KeyPresses, self).__init__()
        self.keyPresses = keyPresses
        self.interval = interval


    def run(self):
        time.sleep(GUI_WAIT)
        pyautogui.typewrite(self.keyPresses, interval=self.interval)


class TestBoolBox(unittest.TestCase):
    def _message_box_test(self, msgBoxFunc):
            for enterKey in ('enter', ' '):
                t = KeyPresses([enterKey])
                t.start()
                self.assertEqual(msgBoxFunc(), 1)

                t = KeyPresses(['right', enterKey])
                t.start()
                self.assertEqual(msgBoxFunc(), 0)

                t = KeyPresses(['right', 'left', enterKey])
                t.start()
                self.assertEqual(msgBoxFunc(), 1)

                t = KeyPresses(['tab', enterKey])
                t.start()
                self.assertEqual(msgBoxFunc(), 0)

                t = KeyPresses(['tab', 'tab', enterKey])
                t.start()
                self.assertEqual(msgBoxFunc(), 1)

                # Test for all the keyword arguments.
                t = KeyPresses([enterKey])
                t.start()
                self.assertEqual(msgBoxFunc(msg="Shall I continue?", title=" ", choices=("Yes", "No"), image=None), 1)


    def test_ynbox(self):
        self._message_box_test(easygui.ynbox)


    def test_ccbox(self):
        self._message_box_test(easygui.ynbox)


    def test_boolbox(self):
        self._message_box_test(easygui.boolbox)


class TestIndexBox(unittest.TestCase):
    def test_indexbox(self):
        for enterKey in ('enter', ' '):
            t = KeyPresses([enterKey])
            t.start()
            self.assertEqual(easygui.indexbox(), 0)

            t = KeyPresses(['right', enterKey])
            t.start()
            self.assertEqual(easygui.indexbox(), 1)

            t = KeyPresses(['right', 'left', enterKey])
            t.start()
            self.assertEqual(easygui.indexbox(), 0)

            t = KeyPresses(['tab', enterKey])
            t.start()
            self.assertEqual(easygui.indexbox(), 1)

            t = KeyPresses(['tab', 'tab', enterKey])
            t.start()
            self.assertEqual(easygui.indexbox(), 0)

            # Test for all the keyword arguments.
            t = KeyPresses([enterKey])
            t.start()
            self.assertEqual(easygui.indexbox(msg="Shall I continue?", title=" ", choices=("Yes", "No"), image=None), 0)

            # test 3 buttons
            t = KeyPresses(['tab', 'tab', enterKey])
            t.start()
            self.assertEqual(easygui.indexbox(choices=('A', 'B', 'C')), 2)

            # test 4 buttons
            t = KeyPresses(['tab', 'tab', 'tab', enterKey])
            t.start()
            self.assertEqual(easygui.indexbox(choices=('A', 'B', 'C', 'D')), 3)

            # test 5 buttons
            t = KeyPresses(['tab', 'tab', 'tab', 'tab', enterKey])
            t.start()
            self.assertEqual(easygui.indexbox(choices=('A', 'B', 'C', 'D', 'E')), 4)


class TestButtonBox(unittest.TestCase):
    def test_msgbox(self):
        for enterKey in ('enter', ' '):
            t = KeyPresses([enterKey])
            t.start()
            self.assertEqual(easygui.msgbox(), 'OK')

            # Test for all the keyword arguments.
            t = KeyPresses([enterKey])
            t.start()
            self.assertEqual(easygui.msgbox(msg='(Your message goes here)', title=' ', ok_button='OK', image=None, root=None), 'OK')


    def test_buttonbox(self):
        for enterKey in ('enter', ' '):
            t = KeyPresses([enterKey])
            t.start()
            self.assertEqual(easygui.buttonbox(), 'Button1')

            # test 3 buttons
            t = KeyPresses(['tab', 'tab', enterKey])
            t.start()
            self.assertEqual(easygui.buttonbox(choices=('A', 'B', 'C')), 'C')

            # test 4 buttons
            t = KeyPresses(['tab', 'tab', 'tab', enterKey])
            t.start()
            self.assertEqual(easygui.buttonbox(choices=('A', 'B', 'C', 'D')), 'D')

            # test 5 buttons
            t = KeyPresses(['tab', 'tab', 'tab', 'tab', enterKey])
            t.start()
            self.assertEqual(easygui.buttonbox(choices=('A', 'B', 'C', 'D', 'E')), 'E')

            # Test for all the keyword arguments.
            t = KeyPresses([enterKey])
            t.start()
            self.assertEqual(easygui.buttonbox(msg='',title=' ', choices=('Button1', 'Button2', 'Button3'), image=None, root=None), 'Button1')


class TestEnterBox(unittest.TestCase):
    def test_integerbox(self):
        for number in (0, 9, 42):
            t = KeyPresses(list(str(number)) + ['enter'])
            t.start()
            self.assertEqual(easygui.integerbox(), number)

        # Test for invalid number range (too small)
        t = KeyPresses(['-', '1', 'enter', 'enter', '8', 'enter'], interval=0.25)
        t.start()
        self.assertEqual(easygui.integerbox(), 8)

        # Test for invalid number range (too large)
        t = KeyPresses(['9', '9', '9', 'enter', 'enter', '8', 'enter'], interval=0.25)
        t.start()
        self.assertEqual(easygui.integerbox(), 8)

        # Test escape key press
        t = KeyPresses(['escape'], interval=0.25)
        t.start()
        self.assertEqual(easygui.integerbox(), None)


if __name__ == '__main__':
    unittest.main()