'''
Created on Oct 13, 2011

@author: obartley
'''

from com.android.monkeyrunner import MonkeyRunner
import commands

def adb(args):
    cmd = 'adb ' + args
    return commands.getoutput(cmd)

def devicePicker():
    deviceList = adb('devices')[len('List of devices attached'):].split()
    deviceList = filter (lambda i: i != 'device', deviceList)    
    rv = MonkeyRunner.choice('Select a device', deviceList)
    return deviceList[rv]
