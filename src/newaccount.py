'''
Created on Oct 12, 2011

@author: obartley
'''

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from time import sleep
from sys import exit

#deviceID = '1000bb29eaa0' #Tab 7
#deviceID = 'HT0BEP800110' # N1
deviceID = 'HT0B3HL15137'
#deviceID = 'emulator-5554'
startComponent = 'com.paypal.android.p2pmobile/.activity.GridLauncherActivity'

dev = MonkeyRunner.waitForConnection(10, deviceID)

if (dev == None):
    print("Couldn't get a reference to a device")
    exit()
    
dev.startActivity(component = startComponent)
MonkeyRunner.alert("If you haven't agreed to the PayPal terms or configured debug options, do so now before clicking OK") 

testUSID = MonkeyRunner.input(message = "Enter a unique session number:", initialValue = '0')
userEmail = MonkeyRunner.input(message = "Enter the new user's email address:", initialValue = 'user' + testUSID + '@deadbeef.com')
userPassword = MonkeyRunner.input(message = "Enter the new user's password:", initialValue = '11111111')
userMobile = testUSID[-4:].rjust(4, '0')
userMobile = MonkeyRunner.input(message = "Enter the new user's phone number:", initialValue = '503467' + userMobile)


dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_CENTER', MonkeyDevice.DOWN_AND_UP)
sleep(1)

# Page one of create user
dev.type(userEmail)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.type(userPassword)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.type(userPassword)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
#  country selector
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_CENTER', MonkeyDevice.DOWN_AND_UP)
sleep(3)

# Page two
dev.type('Chuck')
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.type('Q')
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.type('Testa')

dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.type(userMobile)

dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)

#address fields
dev.type( testUSID )
dev.press('KEYCODE_SPACE', MonkeyDevice.DOWN_AND_UP)
dev.type('Foobar')
dev.press('KEYCODE_SPACE', MonkeyDevice.DOWN_AND_UP)
dev.type('Street')

dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.type ( 'Apartment')
dev.press('KEYCODE_SPACE', MonkeyDevice.DOWN_AND_UP)
dev.type ( '#' + testUSID[-1:] )

dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.type('Portland')

#end address fields


dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_CENTER', MonkeyDevice.DOWN_AND_UP)
#OR = state #46
for i in range(46):
    dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_CENTER', MonkeyDevice.DOWN_AND_UP)
sleep(1)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.type('97205')
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_CENTER', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
