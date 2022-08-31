#程式需求:
#須回應錯誤代碼
#需可建立目前閘門狀態
#
from SerialTest import SerialCtrl
from Utility import CMDlink
from  Judge import CheckCMDType

def DisplayCmdLinks(CmdlinksInfo):
    i=0
    for x in CmdlinksInfo.keys():
       i+=1
       print('{}.{}'.format(i,x))




TestModeList=['User','Serial']

TestMode=TestModeList[0]


if TestMode=='Serial':
    #連接埠設定
    ser=SerialCtrl()
    AvailblePort=ser.serial_ports()
    if len(AvailblePort)==1:
        ComNumber=AvailblePort[0]
    else:
        Number=input('請輸入連接埠數值')
        ComNumber='COM'+Number
    try:
        ser.ConnectSerial(ComNumber, '57600')
    except:
        print('連接失敗')

    while(1):
        ser.GetDebugInfo()
else:
    CMDL=CMDlink()
    CmdFileName=CMDL.GetCMDGroup()
    CmdlinksInfo=CMDL.CmdlinksIndo(CmdFileName)
    DisplayCmdLinks(CmdlinksInfo)
    print()
    CmdlinksList=[]
    for x in CmdlinksInfo.keys():
        CmdlinksList.append(x)

    UserCmd=input('請輸入')


#批量測試使用
    # for UserCmd in range(len(CmdlinksList)):
    #     CmdName = CmdlinksList[UserCmd]
    #     cmd = CmdlinksInfo[CmdName]['commmand']
    #     cmd = CMDL.GetHexCommand(cmd)
    #     CheckCMDType(cmd)