from Utility import CMDlink

#Request Format Define
#----------------------------------------
D = 0
S = 1
LEN=2
CLA = 3
INS = 4
P1 = 5
P2 = 6
LC=7
LE=-2

#-------------------------------------------

def CheckEDC(cmd):
    EDC=0
    for x in range(len(cmd)-1):
        EDC^=cmd[x]
    if cmd[-1]==EDC:
        return True
    else:
        print('TrueEDC =',EDC)
        return False

def CheckCmdTypeLen(cmd,CMDType):
    CommandLemDict={
        'PLC Reboot':0x05,
        'PLC Firmware Version':0x05,
        'Flap Action':0x05,
        'Flap Position':0x05,
        'Set Direction Mode':0x05,
        'Set Parameters':0x09,
        'Save and Query Parameters':0x05,
        'Following Alert':0x05
    }
    if cmd[2]==CommandLemDict[CMDType]:
        return True
    else:
        return False


def CheckCMDType(cmd):
    CMDTypeList = []
    f=open('KSGate_CommandTypeList.text')
    for x in f.readlines():
        CMDTypeList.append(x.rstrip())
    if cmd[CLA] == 0x90:
        if cmd[INS] == 0x00:
            CMDType = CMDTypeList[0]
        elif cmd[INS] == 0x10:
            CMDType = CMDTypeList[1]
    elif cmd[CLA] == 0x81:
        if cmd[INS] == 0x10:
            CMDType = CMDTypeList[2]
        elif cmd[INS] == 0x20:
            CMDType = CMDTypeList[3]
        elif cmd[INS] == 0x30:
            CMDType = CMDTypeList[4]
        elif cmd[INS] == 0x40:
            CMDType = CMDTypeList[5]
        elif cmd[INS] == 0x50:
            CMDType = CMDTypeList[6]
        elif cmd[INS] == 0x90:
            CMDType = CMDTypeList[7]
    else:
        CMDType = 'ErrCMDType'

    return CMDType

def AdvenceCheck(cmd,CMDType):
    EasyCMDL=CMDlink()
    EasyCmdlinksInfo = EasyCMDL.CmdlinksInfo('System','EasyCmds.csv')
    EasyTypeList=[]
    for x in EasyCmdlinksInfo.keys():
        EasyTypeList.append(x.rstrip())
    CheckEasyCMDType=CMDType in EasyTypeList

    if CheckEasyCMDType==True:
        TrueCmdList = EasyCmdlinksInfo[CMDType]['commmand']
        TrueCmdBytesArray = EasyCMDL.GetHexCommand(TrueCmdList)
        CmdErrindex = []

        for x in range(len(cmd)):
            if cmd[x]!=TrueCmdBytesArray[x]:
                CmdErrindex.append(x)
        if len(CmdErrindex)==0:
            # print(CMDType+' Success')
            return CMDType
        else:
            print('CmdErrindex:',CmdErrindex)

    else:
        if CMDType=='Flap Action':
            FlapAction_OpenA=bytearray([0x02,0xff,0x05,0x81,0x10,0x00,0x00,0x00,0x69])
            FlapAction_Close = bytearray([0x02, 0xff, 0x05, 0x81, 0x10, 0x00, 0x02, 0x00, 0x6b])
            FlapAction_OpenB=bytearray([0x02, 0xff, 0x05, 0x81, 0x10, 0x00, 0x01, 0x00, 0x68])
            if cmd==FlapAction_OpenA:
                print('FlapAction_OpenA')
                return CMDType
            elif cmd==FlapAction_OpenB:
                print('FlapAction_OpenB')
                return CMDType
            elif cmd == FlapAction_Close:
                print('FlapAction_Close')
            else:
                CMDType='ErrCMDType'
                print('ErrCMDType')
        elif CMDType=='Set Direction Mode':
            DirectionModeType={
                0x00: 'Inhibit mode',
                0x01: 'Auto mode',
                0x02: 'Command mode',
                0x03: 'Command open,auto close mode'
            }

            for x in DirectionModeType.keys():
                if cmd[5]==x:
                    print('A Direction'+DirectionModeType[x])
                if cmd[6]==x:
                    print('B Direction'+DirectionModeType[x])
                return CMDType
        elif CMDType=='Set Parameters':
            if cmd[P1]==0x00 & cmd[P2]<=0x01 &cmd[LC]==0x04 & cmd[8]<=0x01:
                if cmd[9]>=cmd[11]:
                    print('Warn Longer then TimeOut!!')
                return CMDType
            else:
                CMDType = 'ErrCMDType'
                print('ErrCMDType')
        elif CMDType=='Save and Query Parameters':
            if cmd[P1]==0x00 & cmd[P2]<=0x01:
                return CMDType
            else:
                CMDType = 'ErrCMDType'
                print('ErrCMDType')
        else:
            CMDType = 'ErrCMDType'
            print('ErrCMDType')
        return CMDType




# def BasicReturnCodeFuc(CMDType):
#     D=0xff
#     S=0x02
#     ReturnData=[]
#     APDU_OK=[0x90,0x00]
#
#     if CMDType=='PLC Reboot':
#         ReturnData=APDU_OK
#
#     elif CMDType=='PLC Firmware Version':
#
#         MachineTypeName = 'PLA'
#         MachineVerInfo=[]
#         for x in MachineTypeName:
#             MachineVerInfo.append(ord(x))
#
#         MachineVersion = [0x20,0x19,0x01,0x09,0x00]
#
#         for x in MachineVersion:
#             MachineVerInfo.append(x)
#
#         for x in APDU_OK:
#             MachineVerInfo.append(x)
#
#         ReturnData=MachineVerInfo
#
#     elif CMDType=='Flap Action':
#         ReturnData = APDU_OK
#
#     elif CMDType=='Flap Position':
#         GateStatusDict={'OPENA':0x00,'OPENB':0x01,'CLOSE':0x02,'MOVING':0x03,'UNKNOW':0x04}
#         GateStatusList=[]
#         GateStatusList.append(GateStatusDict['UNKNOW'])
#         for x in APDU_OK:
#             GateStatusList.append(x)
#         ReturnData = GateStatusList
#
#     elif CMDType=='Flap Position':
#         ReturnData = APDU_OK
#
#     elif CMDType=='Set Direction Mode':
#         ReturnData = APDU_OK
#
#     elif CMDType=='Set Parameters':
#         ReturnData = APDU_OK
#
#
# #-------------------------------------------------------------------------------
#     ReturnCodeLen=len(ReturnData)
#     ReturnCodeList=[]
#
#     ReturnCodeList.append(D)
#     ReturnCodeList.append(S)
#     ReturnCodeList.append(ReturnCodeLen)
#     for x in ReturnData:
#         ReturnCodeList.append(x)
#
#     EDC=0
#     for x in ReturnCodeList:
#         EDC^=x
#     ReturnCodeList.append(EDC)
#     ReturnCode = bytearray()
#     for x in ReturnCodeList:
#         ReturnCode.append(x)
#
#     return ReturnCode

def CrudeReturnCode(CMDType):
    D = 0xff
    S = 0x02
    ReturnData = []
    APDU_OK = [0x90, 0x00]
    #-----------------------------------------------------------------------------------
    if CMDType == 'PLC Reboot':
        ReturnData = APDU_OK
    elif CMDType == 'PLC Firmware Version':

        MachineTypeName = 'PLA'
        MachineVerInfo = []
        for x in MachineTypeName:
            MachineVerInfo.append(ord(x))

        MachineVersion = [0x20, 0x19, 0x01, 0x09, 0x00]

        for x in MachineVersion:
            MachineVerInfo.append(x)

        for x in APDU_OK:
            MachineVerInfo.append(x)

        ReturnData = MachineVerInfo
    elif CMDType == 'Flap Action':
        ReturnData = APDU_OK
    elif CMDType == 'Flap Position':
        GateStatusDict = {'OPENA': 0x00, 'OPENB': 0x01, 'CLOSE': 0x02, 'MOVING': 0x03, 'UNKNOW': 0x04}
        GateStatusList = []
        GateStatusList.append(GateStatusDict['OPENB'])
        for x in APDU_OK:
            GateStatusList.append(x)
        ReturnData = GateStatusList
    elif CMDType == 'Set Direction Mode':
        ReturnData = APDU_OK
    elif CMDType == 'Set Parameters':
        ReturnData = APDU_OK
    elif CMDType=='Save and Query Parameters':
        ReturnData=[0x14,0x01,0x19,0x20,0x03,0x01,0x00,0x00,0x01,0x02,0x01,0x05,0x00,0x05,0x03,0x0A,0x90,0x00]
    elif CMDType == 'Following Alert':
        ReturnData = [0x00,0x00,0x00,0x00,0x00,0x00,0x90,0x00]

    # -------------------------------------------------------------------------------
    ReturnCodeLen = len(ReturnData)
    ReturnCodeList = []

    ReturnCodeList.append(D)
    ReturnCodeList.append(S)
    ReturnCodeList.append(ReturnCodeLen)
    for x in ReturnData:
        ReturnCodeList.append(x)

    EDC = 0
    for x in ReturnCodeList:
        EDC ^= x
    ReturnCodeList.append(EDC)
    ReturnCode = bytearray()
    for x in ReturnCodeList:
        ReturnCode.append(x)

    return ReturnCode


def DisplayCmdLinks(CmdlinksInfo):
    i=0
    for x in CmdlinksInfo.keys():
       i+=1
       print('{}.{}'.format(i,x))


if __name__ == '__main__':
    CMDL=CMDlink()
    CmdFileName=CMDL.GetCMDGroup()
    CmdlinksInfo=CMDL.CmdlinksIndo(CmdFileName)
    #DisplayCmdLinks(CmdlinksInfo)
    print()
    CmdlinksList=[]
    for x in CmdlinksInfo.keys():
        CmdlinksList.append(x)

    #UserCmd=input('請輸入')

    for UserCmd in range(len(CmdlinksList)):
        CmdName = CmdlinksList[UserCmd]
        print(CmdName)
        cmd = CmdlinksInfo[CmdName]['commmand']
        cmd = CMDL.GetHexCommand(cmd)


        CheckCMDType(cmd)
