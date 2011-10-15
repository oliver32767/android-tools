'''
Created on Oct 15, 2011

@author: waxwing
'''
import os, sys, commands
from com.android.monkeyrunner import MonkeyRunner
if __name__ == '__main__':
                 
    monkeys =  os.listdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    monkeys = filter (lambda m: m[-3:] == '.py', monkeys)
    try:
        monkeys.remove('main.py')
        monkeys.remove('monkeytools.py')
    except (ValueError):
        pass

    m = MonkeyRunner.choice('Select a script', monkeys)
    if m != -1:
        commands.getoutput('monkeyrunner ' + monkeys[m])