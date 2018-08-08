import pyautogui as pgui
import pywinauto as pwin
from win32com.client import GetObject
from pywinauto import application
import time
import os
import subprocess

#print(pgui.size())
#print("location: ")
#print(pgui.locateOnScreen(refpics_path + '/search_bar.PNG'))
#print()
# pgui.click(pgui.center(pgui.locateOnScreen(refpics_path + '/stop_button.PNG')))  # Dumb line that stops script
#while True:
#    try:
#        x, y, w, h = pgui.locateOnScreen(refpics_path + '/search_bar.PNG')
#    except TypeError:
#        print('Reference image not found on screen...')
#        time.sleep(2)
#    try:
#        ctrx, ctry = pgui.center((x, y, w, h))
#        print(ctrx, ctry)
#        pgui.click((ctrx, ctry))
#        pgui.typewrite('Hello World!')
#        pgui.press('enter')
#        time.sleep(2)
#    except:
#        print('Reference img. not found on screen')
#        time.sleep(1)
class NardaNavigator():

    def __init__(self):
        pgui.PAUSE = 0
        self.refpics_path = '../narda_navigator_referencepics'
        self.ehp200_path = "C:\\Program Files (x86)\\NardaSafety\\EHP-TS\\EHP200-TS\\EHP200.exe"
        self.ehp200_app = application.Application()
        self.startNarda()

    def startNarda(self):
        WMI = GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        p_list = [p.Properties_('Name').Value for p in processes]
        print(p_list)
        # ehp200_app = pwin.Application()
        if self.ehp200_path.split('\\')[-1] not in p_list:
            print("Starting EHP200 program - Connecting...")
            self.ehp200_app.start(self.ehp200_path)
            # Wait until the window has been opened
            while not pgui.locateOnScreen(self.refpics_path + '/window_title.PNG'):
                pass
            print("EHP200 Opened")
        else:
            print("EHP200 already opened - Connecting...")
            self.ehp200_app.connect(path=self.ehp200_path)

    def closeNarda(self):
        self.ehp200_app.kill()

    def selectModeTab(self):
        try:
            if not pgui.locateOnScreen(self.refpics_path + '/mode_tab_selected.PNG'):
                x, y, w, h = pgui.locateOnScreen(self.refpics_path + '/mode_tab_deselected.PNG')
                print(x, y, w, h)
                # x_save, y_save = saveCurrentLocation()
                pgui.click(pgui.center((x, y, w, h)))
                # loadSavedLocation(x_save, y_save)
            else:
                print("Already in the 'Mode' tab")
        except TypeError:
            print('Reference image not found on screen...')
            exit(1)

    def selectTab(self, tabName):
        tabName = tabName.lower()
        print(tabName)
        selectedName = '/' + tabName + '_tab_selected.PNG'
        deselectedName = '/' + tabName + '_tab_deselected.PNG'
        print(selectedName, deselectedName)
        try:
            if not pgui.locateOnScreen(self.refpics_path + selectedName):
                print("Not located - clicking the position: " + self.refpics_path + deselectedName)
                x, y, w, h = pgui.locateOnScreen(self.refpics_path + '/' + tabName + '_tab_deselected.PNG',
                                                 grayscale=True)
                print(x, y, w, h)
                pgui.click(pgui.center((x, y, w, h)))
            else:
                print("Already in the '" + tabName + "' tab")
        except TypeError:
            print('Error: Reference images not found on screen...')
            exit(1)

    def saveCurrentLocation(self):
        return pgui.position()

    def loadSavedLocation(self, x, y):
        pgui.moveTo(x, y)

    def bringToFront(self):
        self.ehp200_app.EHP200.set_focus()

    def main(self):
        self.startNarda()
        self.bringToFront()
        self.selectTab('Mode')
        time.sleep(0.5)
        self.selectTab('Data')
        time.sleep(0.5)
        self.selectTab('Data')
        time.sleep(0.5)
        self.selectTab('Span')
        time.sleep(0.5)
        self.selectTab('Span')
        time.sleep(0.5)
        self.selectTab('Mode')

if __name__ == '__main__':
    ehp200 = NardaNavigator()
    ehp200.main()
