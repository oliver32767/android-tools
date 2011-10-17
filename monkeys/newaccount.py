'''
Created on Oct 12, 2011

@author: obartley
'''

from sys import exit
from monkeytools import devicePicker, EvilMonkey, MonkeyRunner

dev = EvilMonkey(devicePicker())
if (dev == None):
    MonkeyRunner.alert("Couldn't get a reference to a device")
    exit()

startComponent = 'com.paypal.android.p2pmobile/.activity.GridLauncherActivity'

    
dev.startActivity(component = startComponent)
MonkeyRunner.alert("If you haven't agreed to the PayPal terms or configured debug options, do so now before clicking OK") 

testUSID = MonkeyRunner.input(message = "Enter a unique session number:", initialValue = '0')
userEmail = MonkeyRunner.input(message = "Enter the new user's email address:", initialValue = 'user' + testUSID + '@deadbeef.com')
userPassword = MonkeyRunner.input(message = "Enter the new user's password:", initialValue = '11111111')
userMobile = testUSID[-4:].rjust(4, '0')
userMobile = MonkeyRunner.input(message = "Enter the new user's phone number:", initialValue = '503467' + userMobile)
userZIP = MonkeyRunner.input(message = "Enter the new user's ZIP code:", initialValue = '97205')


# from the main login screen:
dev.sequence('N' + 'd' * 5 + 'c,,')

# Page one of create user
dev.type(userEmail)
dev.sequence('d')
dev.type(userPassword)
dev.sequence('d')
dev.type(userPassword)
dev.sequence('ddc,,')

# Page two
dev.sequence('/Chuck/ d /Q/ d /Testa/ d')
dev.type(userMobile)
dev.sequence('d')

#address fields
dev.type( testUSID + ' Foobar Street')
dev.sequence('d')
dev.type ( 'Apartment #' + testUSID[-1:])
dev.sequence('d/Portland')

# state and ZIP
dev.sequence('dc' + 'd' * 46 + 'c,,')
dev.sequence('d/' + userZIP + '/dc' + ('d' * 7)) # now that is some shorthand!
