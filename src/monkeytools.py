'''
Created on Oct 13, 2011

@author: obartley
'''

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from stoat import adb
import commands


class EvilMonkey():
    '''
    This class wraps MonkeyDevice and provides new methods.
    I'm pretty sure that in order to properly inherit from MonkeyDevice
    would require porting all of this over to Jython, but I don't feel like 
    doing it right now. :/
    '''

    def _connect(self):
        '''
        Handles making a connection to the device as well as mappint methods and values
        of the device to exposed methods.
        '''
        
        
        self._device = MonkeyRunner.waitForConnection(self.connectionTimeout, self.deviceId)
        # bogus wrapper stuff, because for some reason I can't inherit 
        # from a jython class
        self.DOWN = self._device.DOWN
        self.UP = self._device.UP
        self.DOWN_AND_UP = self._device.DOWN_AND_UP
        
        # comment out the methods as they get overridden
        self.broadcastIntent = self._device.broadcastIntent
        self.drag = self._device.drag
        self.getProperty = self._device.getProperty
        self.getSystemProperty = self._device.getSystemProperty
        self.installPackage = self._device.installPackage
        self.instrument = self._device.instrument
        self.press = self._device.press
        self.reboot = self._device.reboot
        self.removePackage = self._device.removePackage
        self.shell = self._device.shell
        self.startActivity = self._device.startActivity
        self.takeSnapshot = self._device.takeSnapshot
        self.touch = self._device.touch
        #self.type = self._device.type
        self.wake = self._device.wake
    
    def __init__(self, deviceId, connectionTimeout = 10):
        '''
        Constructor
        '''
        self.connectionTimeout = connectionTimeout
        self.deviceId = deviceId
        self.longPressDuration = 1.5
        self._connect()
        

    def type(self, string):
        '''
        This method enhances the type() method of the base MonkeyDevice class and
        adds support for spaces, which the original apparently doesn't support :/
        '''

        for ch in string:
            if ch == ' ':
                self._device.press('KEYCODE_SPACE', MonkeyDevice.DOWN_AND_UP)
            else:
                self._device.type(ch)
           
    def sequence(self, seq):
        '''
        This method accepts a string seq that represents a sequence of keystrokes
        to be translated into the appropriate press() call of _device.
        
        If characters contained in longPressable[] is passed, then the 
        corresponding press will be a long-press

        To repeat a sequence, use the * operator:
            EvilMonkey.sequence( 'llc' + ',' * 4 + 'dc')
        is the same as:
            Evilmonkey.sequence( 'llc,,,,dc' )
            
        Supported characters are:
            u - KEYCODE_DPAD_UP
            d - KEYCODE_DPAD_DOWN
            l - KEYCODE_DPAD_LEFT
            r - KEYCODE_DPAD_RIGHT
            c - KEYCODE_DPAD_CENTER
            
            h - KEYCODE_HOME
            b - KEYCODE_BACK
            m - KEYCODE_MENU
            s - KEYCODE_SEARCH
            
            > - newline
            < - backspace (del)
        
            , - comma adds a 0.5 second pause
            . - period adds a 2 second pause

        To send a literal portion of a sequence to EvilMonkey.type(), escape the sequence with
        backticks ` or slashes / 
        
        Unless within an escaped literal, spaces and other characters are ignored, allowing you to visually group steps:
            EvilMonkey.sequence( 'dddc /escaped literal/ dc `foo/bar`')
            
            * note that 'foo/bar' is a string literal (the slash is ignored because
            backticks were used to escape this literal)
        '''
       
        longPressable = ('C', 'H', 'B', 'M', 'S')
        keycodeDict = {
                       'u': 'KEYCODE_DPAD_UP',
                       'd': 'KEYCODE_DPAD_DOWN',
                       'l': 'KEYCODE_DPAD_LEFT',
                       'r': 'KEYCODE_DPAD_RIGHT',
                       'c': 'KEYCODE_DPAD_CENTER',
        
                       'h': 'KEYCODE_HOME',
                       'b': 'KEYCODE_BACK',
                       'm': 'KEYCODE_MENU',
                       's': 'KEYCODE_SEARCH',
                       'n': 'KEYCODE_ENTER',
                       'b': 'KEYCODE_DEL'
                       }
        
        escapeChars = ('`', '/')
        pauseChars = {',': 0.5, '.': 2}
        
        keycode = None
                
        for ch in seq:
            if keycode is None:
                # if keycode is none, that means ch isn't literal
                if ch in escapeChars:
                    # begin escaping a literal
                    keycode = ch
                    
                elif ch in pauseChars.keys():
                    # pause for the time associated with ch as key
                    MonkeyRunner.sleep(pauseChars[ch])
                    
                else:        
                    try: # check if ch is in the dictionary, if not
                        # the error is caught and we don't do anything
                        # this way, anything not explicitly listed is ignored
                        keycode = keycodeDict[ch.lower()]
                        if ch in longPressable:
                            # long-press 
                            self._device.press(keycode, MonkeyDevice.DOWN)
                            MonkeyRunner.sleep(self.longPressDuration)
                            self._device.press(keycode, MonkeyDevice.UP)
                        else:
                            # tap
                            self._device.press(keycode, MonkeyDevice.DOWN_AND_UP)
                            
                    except (KeyError):
                        # this means ch was not in the dictionary, it's an ignored character
                        pass
                    keycode = None
                    
            else:
                # that mean's this ch is a literal
                if ch == keycode:
                    # stop escaping
                    keycode = None
                else:
                    self.type(ch)

                    


def devicePicker():
    deviceList = adb('devices')[len('List of devices attached'):].split()
    deviceList = filter (lambda i: i != 'device', deviceList)    
    rv = MonkeyRunner.choice('Select a device', deviceList)
    return deviceList[rv]
