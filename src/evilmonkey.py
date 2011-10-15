'''
Created on Oct 12, 2011

@author: waxwing
'''

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

class EvilMonkey(MonkeyDevice):
    '''
    This class wraps MonkeyDevice and provides new methods
    '''


    def __init__(self, deviceID):
        '''
        Constructor
        '''
        self._device = MonkeyRunner.waitForConnection(10, deviceID)
    
    
    def types(self, string):
        '''
        This method enhances the type() method of the base MonkeyDevice class and
        adds support for spaces, which the original apparently doesn't support :/
        ''' 
        for ch in str:
            if ch == ' ':
                self._device.press('KEYCODE_SPACE', MonkeyDevice.DOWN_AND_UP)
            else:
                self._device.type(ch)
            
    def sequence(self, seq):
        '''
        This method accepts a string seq that represents a sequence of keystrokes
        to be translated into the appropriate press() call of _device.
        TODO: if characters chbms are capitalized, then long-press
        
        Supported characters are:
        dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
        u - KEYCODE_DPAD_UP
        d - KEYCODE_DPAD_DOWN
        l - KEYCODE_DPAD_LEFT
        r - KEYCODE_DPAD_RIGHT
        c - KEYCODE_DPAD_CENTER
        
        h - KEYCODE_HOME
        b - KEYCODE_BACK
        m - KEYCODE_MENU
        s - KEYCODE_SEARCH
        
        . - adds a 0.5 second pause
        
        an example would be seq = 'dddC..rrddc'
        '''
        for ch in seq:
            if ch == 'u':
                key = 'KEYCODE_DPAD_UP'
            elif ch == 'd':
                key == 'KEYCODE_DPAD_DOWN'
            elif ch == 'l':
                key == 'KEYCODE_DPAD_LEFT'
            elif ch == 'r':
                key == 'KEYCODE_DPAD_RIGHT'
            elif ch == 'c' or ch == 'C':
                key == 'KEYCODE_DPAD_CENTER'
            elif ch == 'h' or ch == 'H':
                key == 'KEYCODE_HOME'
            elif ch == 'b' or ch == 'B':
                key == 'KEYCODE_BACK'
            elif ch == 'm' or 'M':
                key == 'KEYCODE_MENU'
            elif ch == 's' or ch == 'S':
                key == 'KEYCODE_SEARCH'
            elif ch =='.':
                key == None
                MonkeyRunner.sleep(0.5)
            else:
                key = None
            
            if key is not None:
                if key.isupper():
                    self._device.press(key, MonkeyDevice.DOWN)
                    MonkeyRunner.sleep(0.5)
                    self._device.press(key, MonkeyDevice.UP)
                else
                    self._device.press(key, MonkeyDevice.DOWN_AND_UP)
                    
                
                
                