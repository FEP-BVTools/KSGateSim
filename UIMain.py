from SerialTest import SerialCtrl
from Utility import CMDlink
from  Judge import CheckCMDType,AdvenceCheck,CheckEDC,CrudeReturnCode,CheckCmdTypeLen
import tkinter as tk
from tkinter import ttk
import threading

ser = SerialCtrl()

start_threads=False

def JudgeFuc():
 while (1):
  cmd = ser.GetDebugInfo()
  if len(cmd) != 0:
   if CheckEDC(cmd) == True:
    CMDType = CheckCMDType(cmd)
    CommandTypeWord.set(CMDType)
    if CMDType == 'ErrCMDType':
     print(CMDType)
    else:
     if CheckCmdTypeLen(cmd, CMDType) == True:
      CMDType = AdvenceCheck(cmd, CMDType)
      print(CMDType)
      ModeType=TypeVar.get()
      if ModeType=='APDU_ERR Mode':
          CMDType='ErrResponse'
      ReturnCode = CrudeReturnCode(CMDType)
      # for x in ReturnCode:
      # print(hex(x).upper()[2::],end=' ')
      ser.SerialWrite(ReturnCode)
     else:
      print('CommandLen Error')
   else:
    print('EDC Error')


def sel():
 a=TypeVar.get()
 CommandTypeWord.set(TypeVar.get())
 print(a)
 if a=='Normal Mode':
   frame.config(bg='green')
 elif a== 'APDU_ERR Mode':
  frame.config(bg='red')

#下拉式選單被觸發
def callbackFunc(event):
    try:
        ser.SerialClose()
    except:
        print('COMPort未連接')

    if JudgeFucThread.is_alive():
        ser.start_threads = False
        JudgeFucThread.join()

    ComNumber=COMPortcombo.get()
    try:
        ser.ConnectSerial(ComNumber, '57600')
        COMlabelText.set('{}已連接'.format(ComNumber))
        JudgeFucThread.start()
    except:
        print('連接失敗')


root = tk.Tk()
#視窗標題設置
root.title('KSGateSim')
root.geometry('200x250+300+400')

#指示燈
#創建可容納物件的框架
frame = tk.Frame(root, width=100, height=100)
frame.pack()
# 把 Label 放入 Frame
CommandTypeWord = tk.StringVar()
CommandTypeWord.set('None')
LED=tk.Label(frame, textvariable=CommandTypeWord).place(x=0, y=30)

#COMPort設定
#---------------------------------------------------------------------------------
AvailblePort = ser.serial_ports()
COMlabelText = tk.StringVar()
COMlabelText.set("選擇要連接的COM")
labelTop = tk.Label(root,textvariable=COMlabelText)
labelTop.pack()
COMPortcombo = ttk.Combobox(root,values=AvailblePort)
COMPortcombo.pack()
COMPortcombo.bind("<<ComboboxSelected>>", callbackFunc)

JudgeFucThread = threading.Thread(target=JudgeFuc)

if len(AvailblePort) == 1:
    ComNumber = AvailblePort[0]
    COMPortcombo.current(0)
    try:
        ser.ConnectSerial(ComNumber, '57600')
        COMlabelText.set('{}已連接'.format(ComNumber))
        JudgeFucThread.start()
    except:
        print('連接失敗')
else:
    print(AvailblePort)

#---------------------------------------------------------------------------------


#設定變數 String 型別儲存目前內容
TypeVar = tk.StringVar()
#設置 var 內容
TypeVar.set('Normal')
#新增選項
tk.Radiobutton(root, variable=TypeVar, text='正常', value='Normal Mode',command=sel).pack()
#新增選項
tk.Radiobutton(root, variable=TypeVar, text='錯誤', value='APDU_ERR Mode',command=sel).pack()





#運行視窗
root.mainloop()

