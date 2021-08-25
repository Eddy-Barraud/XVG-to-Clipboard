# pyinstaller --onefile -w ".\XVG-To-Clipboard.py --exclude-module PyQt5"
import PySimpleGUIQt as sg
import pyperclip
import re

class Listbox(sg.Listbox):

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        data = window['LISTBOX'].get_list_values()
        #print(data)
        items = [str(v) for v in e.mimeData().text().strip().split('\n')]
        print(items)
        self.toClipBoard(items[0][8:])
        data.extend(items)
        #print(data)
        window['LISTBOX'].update(data)
        window.refresh()

    def enable_drop(self):
        # Called after window finalized
        self.Widget.setAcceptDrops(True)
        self.Widget.dragEnterEvent = self.dragEnterEvent
        self.Widget.dragMoveEvent = self.dragMoveEvent
        self.Widget.dropEvent = self.dropEvent

    def toClipBoard(self, filename):
        f = open(filename, "r")
        rawData=f.read().split("\n")[:-2]
        f.close()

        #Remove xvg comments
        for i in range(len(rawData)-1,-1,-1):
            if len(re.findall("^[#|@]",rawData[i])) >= 1:
                rawData.pop(i)

        #Split into array of arrays for each frame
        rawDataArr=[rawData[i].split() for i in range(0,len(rawData))]

        result=""
        for line in rawDataArr:
            for value in line:
                result+=f'{value}\t'
            result+=f'\n'
        pyperclip.copy(result)

layout = [[sg.T("Drag and drop an XVG file below and values will be copied to raw data inside your clipboard")],[Listbox([], size=(50, 10), enable_events=True, key='LISTBOX')]]

window = sg.Window("XVG Copy", layout, finalize=True)
window['LISTBOX'].enable_drop()

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    #print(values)

window.close()