'''
Created on Oct 12, 2011

@author: obartley
'''

#from com.android.monkeyrunner import MonkeyRunner
from sys import exit
from monkeytools import devicePicker, EvilMonkey, MonkeyRunner


deviceID = devicePicker()

dev = EvilMonkey(deviceID)

startComponent = 'com.paypal.android.p2pmobile/.activity.GridLauncherActivity'



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


dev.sequence('dddc..')

# Page one of create user
dev.type(userEmail)
dev.sequence('d')
dev.type(userPassword)
dev.sequence('d')
dev.type(userPassword)
dev.sequence('ddc...')

# Page two
dev.type('Chuck')
dev.sequence('d')
dev.type('Q')
dev.sequence('d')
dev.type('Testa')
dev.sequence('d')
dev.type(userMobile)
dev.sequence('d')

#address fields
dev.type( testUSID + ' Foobar Street')
dev.sequence('d')
dev.type ( 'Apartment #' + testUSID[-1:])
dev.sequence('d')
dev.type('Portland')
#end address fields


dev.sequence('dc')
#OR = state #46
#for i in range(46):
#    dev.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
dev.sequence('d', 46)
dev.sequence('c.d')
dev.type('97205')
dev.sequence('dcddddddd')