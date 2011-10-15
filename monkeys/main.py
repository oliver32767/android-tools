'''
Created on Oct 15, 2011

@author: waxwing
'''
import os, sys, commands
from com.android.monkeyrunner import MonkeyRunner
if __name__ == '__main__':
    blacklist = ['main.py', 'monkeytools.py']
    
    monkeys =  os.listdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    monkeys = filter (lambda m: m[-3:] == '.py', monkeys)
    monkeys = filter (lambda m: m not in blacklist, monkeys)
    m = MonkeyRunner.choice('Select a script', monkeys)
    if m != -1:
        commands.getoutput('monkeyrunner ' + monkeys[m])