'''
Created on Oct 13, 2011

@author: obartley
'''

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import commands



class EvilMonkey():
    '''
    This class wraps MonkeyDevice and provides new methods.
    I'm pretty sure that in order to properly inherit from MonkeyDevice
    would require porting all of this over to Jython, but I don't feel like 
    doing it right now. :/
    '''

    @property
    def deviceId(self):
        '''Device ID of the connected device'''
        def fget():
            return self._deviceId
        def fset(value):
            print('Device ID updated to %s' % value)
            if value == None:
                self._device = None
            else:
                self._deviceId = value
                self._connect()
                
    def _connect(self):
        '''
        Handles making a connection to the device as well as mappint methods and values
        of the device to exposed methods.
        '''
        
        self._device = MonkeyRunner.waitForConnection(self.connectionTimeout, self._deviceId)
        # bogus wrapper stuff
        self.DOWN = self._device.DOWN
        self.UP = self._device.UP
        self.DOWN_AND_UP = self._device.DOWN_AND_UP
        
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
        self._deviceId = deviceId
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
           
    def sequence(self, seq, repeat = 1):
        '''
        This method accepts a string seq that represents a sequence of keystrokes
        to be translated into the appropriate press() call of _device.
        If characters chbms are capitalized, then long-press
        The sequence will be repeated as specified by the repeat parameter. 
        
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

        if repeat <= 0:
            break

        for ch in seq * repeat:
            keycode = None
            if ch == 'u':
                keycode = 'KEYCODE_DPAD_UP'
            elif ch == 'd':
                keycode = 'KEYCODE_DPAD_DOWN'
            elif ch == 'l':
                keycode = 'KEYCODE_DPAD_LEFT'
            elif ch == 'r':
                keycode = 'KEYCODE_DPAD_RIGHT'
            elif ch == 'c' or ch == 'C':
                keycode = 'KEYCODE_DPAD_CENTER'
            elif ch == 'h' or ch == 'H':
                keycode = 'KEYCODE_HOME'
            elif ch == 'b' or ch == 'B':
                keycode = 'KEYCODE_BACK'
            elif ch == 'm' or ch == 'M':
                keycode = 'KEYCODE_MENU'
            elif ch == 's' or ch == 'S':
                keycode = 'KEYCODE_SEARCH'
            elif ch == '.':
                MonkeyRunner.sleep(0.5)
            
            if keycode is not None:
                if ch.isupper():
                    self._device.press(keycode, MonkeyDevice.DOWN)
                    MonkeyRunner.sleep(self.longPressDuration)
                    self._device.press(keycode, MonkeyDevice.UP)
                else:
                    self._device.press(keycode, MonkeyDevice.DOWN_AND_UP)

def adb(args):
    cmd = 'adb ' + args
    return commands.getoutput(cmd)

def devicePicker():
    deviceList = adb('devices')[len('List of devices attached'):].split()
    deviceList = filter (lambda i: i != 'device', deviceList)    
    rv = MonkeyRunner.choice('Select a device', deviceList)
    return deviceList[rv]
