from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time

#deviceID = '1000bb29eaa0' #Tab 7
deviceID = 'HT0BEP800110' # N1
#deviceID = 'emulator-5554'
startComponent = 'com.paypal.android.p2pmobile/.activity.GridLauncherActivity'

locales = [ (0, 'de_DE'),
            (1, 'en_UK'),
            (2, 'en_US'),
            (3, 'es_ES'),
            (4, 'es_MX'),
            (5, 'fr_FR'),
            (6, 'it_IT'),
            (7, 'pt_PT'),
            (8, 'ru_RU'),
            #(9, 'ko_KR'),
            (10, 'zh_01'),
            (11, 'zh_02'),
            (12, 'jp_JP'),
            ]

def getNewLocale(device, index):
    device.startActivity(component='com.android.settings/.LocalePicker')
    time.sleep(1)
    for i in range(index):
        device.press('KEYCODE_DPAD_DOWN', MonkeyDevice.DOWN_AND_UP)
    device.press('KEYCODE_ENTER', MonkeyDevice.DOWN_AND_UP)


def snapshot(device, locale):
    sshot = device.takeSnapshot()
    sshot.writeToFile('snapshots/' + locale + '.png', 'png')
    
dev = MonkeyRunner.waitForConnection(10, deviceID)
MonkeyRunner.alert('Configure the device now')

for l in locales:
    getNewLocale(dev, l[0]) 
    print(l[1])
    dev.startActivity(component = startComponent)
    time.sleep(1)
    snapshot(dev, l[1])


