#程式需求:
#須回應錯誤代碼
#需可建立目前閘門狀態
#
from SerialTest import SerialCtrl
from Utility import CMDlink
from  Judge import CheckCMDType,AdvenceCheck,CheckEDC,CrudeReturnCode,CheckCmdTypeLen

def DisplayCmdLinks(CmdlinksInfo):
    i=0
    for x in CmdlinksInfo.keys():
       i+=1
       print('{}.{}'.format(i,x))




TestModeList=['User','Serial']

TestMode=TestModeList[1]


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
        cmd=ser.GetDebugInfo()
        if len(cmd)!=0:
            if CheckEDC(cmd)==True:
                CMDType=CheckCMDType(cmd)
                if CMDType=='ErrCMDType':
                    print(CMDType)
                else:
                    if CheckCmdTypeLen(cmd,CMDType)==True:
                        CMDType = AdvenceCheck(cmd, CMDType)
                        print(CMDType)
                        ReturnCode = CrudeReturnCode(CMDType)
                        #for x in ReturnCode:
                            #print(hex(x).upper()[2::],end=' ')
                        ser.SerialWrite(ReturnCode)
                    else:
                        print('CommandLen Error')
            else:
                print('EDC Error')

else:
    CMDL=CMDlink()
    CmdFileName=CMDL.GetCMDGroup('./Commands')
    CmdlinksInfo=CMDL.CmdlinksInfo('Commands',CmdFileName)
    DisplayCmdLinks(CmdlinksInfo)
    print()
    CmdlinksList=[]
    for x in CmdlinksInfo.keys():
        CmdlinksList.append(x)

    # UserCmd=input('請輸入')
    # CmdName = CmdlinksList[eval(UserCmd)-1]
    # cmd = CmdlinksInfo[CmdName]['commmand']
    # cmd = CMDL.GetHexCommand(cmd)
    # if CheckEDC(cmd)==True:
    #     CMDType=CheckCMDType(cmd)
    #     if CheckCmdTypeLen(cmd,CMDType)==True:
    #         CMDType = AdvenceCheck(cmd, CMDType)
    #         print(CMDType)
    #         ReturnCode = CrudeReturnCode(CMDType)
    #         for x in ReturnCode:
    #             print(hex(x).upper()[2::],end=' ')
    #     else:
    #         print('CommandLen Error')
    # else:
    #     print('EDC Error')


#批量測試使用
    for UserCmd in range(len(CmdlinksList)):
        CmdName = CmdlinksList[UserCmd]
        print()
        print('Test:',CmdName)
        cmd = CmdlinksInfo[CmdName]['commmand']
        cmd = CMDL.GetHexCommand(cmd)
        if CheckEDC(cmd)==True:
            CMDType=CheckCMDType(cmd)
            if CheckCmdTypeLen(cmd,CMDType)==True:
                CMDType = AdvenceCheck(cmd, CMDType)
                print(CMDType)
                ReturnCode = CrudeReturnCode(CMDType)
                for x in ReturnCode:
                    print(hex(x).upper()[2::],end=' ')
            else:
                print('CommandLen Error')
        else:
            print('EDC Error')