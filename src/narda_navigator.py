import pyautogui as pgui
import pywinauto as pwin
from win32com.client import GetObject
from pywinauto import application
import time
import os
import subprocess


class NardaNavigator:

    def __init__(self):
        pgui.PAUSE = 0.5
        self.refpics_path = 'narda_navigator_referencepics'
        self.ehp200_path = "C:\\Program Files (x86)\\NardaSafety\\EHP-TS\\EHP200-TS\\EHP200.exe"
        self.snip_path = "C:\\Windows\\System32\\SnippingTool.exe"
        self.ehp200_app = application.Application()
        self.snip_tool = application.Application()
        self.startSnip()
        self.startNarda()

    def startSnip(self):
        WMI = GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        p_list = [p.Properties_('Name').Value for p in processes]
        if self.snip_path.split('\\')[-1] not in p_list:
            print("Starting Snipping Tool - Connecting...")
            self.snip_tool.start(self.snip_path)
            # Wait until the window has been opened
            while not pgui.locateOnScreen(self.refpics_path + '/snip_window_title.PNG'):
                pass
            print("Snipping Tool Opened")
        else:
            print("Snipping Tool Opened")
            self.snip_tool.connect(path=self.snip_path)

    def startNarda(self):
        WMI = GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        p_list = [p.Properties_('Name').Value for p in processes]
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

    def selectTab(self, tabName):
        tabName = tabName.lower()
        # print(tabName)
        selectedName = '/' + tabName + '_tab_selected.PNG'
        deselectedName = '/' + tabName + '_tab_deselected.PNG'
        # print(selectedName, deselectedName)
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

    def selectInputType(self, type):
        if type.lower() == 'elec':
            pass
        elif type.lower() == 'mag_a':
            pass
        elif type.lower() == 'mag_b':
            pass
        else:
            print("Argument must be one of either 'elec', 'mag_a', or 'mag_b'")

    def takeMeasurement(self, dwell_time, filename, pathname):
        self.bringToFront()
        # If not on the data tab, switch to it
        if not pgui.locateOnScreen(self.refpics_path + '/data_tab_selected.PNG'):
            pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/data_tab_deselected.PNG')))

        # Reset measurement by clicking on 'Free Scan' radio button
        pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/free_scan.PNG', grayscale=True)))

        # Todo: figure out if we need to check max hold here too..

        # Wait for the measurements to settle before taking measurements
        time.sleep(dwell_time)

        # Take the actual measurement after marking the highest peak
        pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/highest_peak.PNG', grayscale=True)))
        pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/save_as_text.PNG', grayscale=True)))

        # Input comment
        pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/comment.PNG', grayscale=True)))
        time.sleep(0.5)
        pgui.typewrite("Hello world!")
        pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/ok.PNG', grayscale=True)))

        # Save file
        pgui.typewrite(filename)
        # Change to directory of choice
        pgui.hotkey('ctrl', 'l')
        pgui.typewrite(pathname)
        pgui.press(['enter'])
        try:
            pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/save.PNG', grayscale=True)))
        except TypeError:
            pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/save_underscore.PNG', grayscale=True)))

        # Overwrite if file already exists
        try:
            pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/yes.PNG', grayscale=True)))
            print("File already exists - overwriting file.")
        except TypeError:
            print("New file has been saved.")

        # Wait for file to have saved properly
        while not os.path.isfile(pathname + '/' + filename + '.txt'):
            print(pathname + '/' + filename + '.txt')
            pass

        # Return max recorded value
        return self.getMaxValue(filename, pathname)


    def saveBitmap(self):
        self.bringToFront()
        # Open Data Tab
        if not pgui.locateOnScreen(self.refpics_path + '/data_tab_selected.PNG'):
            pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + 'data_tab_deselected.PNG')))


        # Input comment
        # pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/comment.PNG')))
        # pgui.typewrite("Hello world!")
        # pgui.click(pgui.center(pgui.locateOnScreen(self.refpics_path + '/ok.PNG')))

        # Save file

    def getMaxValue(self, filepath, pathname):
        with open(pathname + '/' + filepath + '.txt', 'r') as f:
            maxValLine = f.readlines()[8]
            for string in maxValLine.split(' '):
                try:
                    maxVal = float(string)
                    break  # Breaks if we find the first numeric value
                except ValueError:
                    continue
            print(maxVal)
        return maxVal

    def saveCurrentLocation(self):
        return pgui.position()

    def loadSavedLocation(self, x, y):
        pgui.moveTo(x, y)

    def bringToFront(self):
        #self.ehp200_app.EHP200.Minimize()
        #self.ehp200_app.EHP200.Restore()
        self.ehp200_app.EHP200.set_focus()

    def bringSnipToFront(self):
        self.snip_tool.SNIP.set_focus()

    def main(self):
        #self.startNarda()
        #self.bringToFront()
        name = "C:\\Users\changhwan.choi\Desktop\L_Efront"
        for i in range(1, 17):
            fname = name + str(i) + ".txt"
            self.getMaxValue(fname)



if __name__ == '__main__':
    ehp200 = NardaNavigator()
    ehp200.main()
