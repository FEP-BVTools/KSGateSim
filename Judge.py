from Utility import CMDlink



def CheckCMDType(cmd):
    CMDTypeList = []
    CLA=3
    INS=4

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
    CheckType=CMDType in EasyTypeList



    if CheckType==True:

        TrueCmdList = EasyCmdlinksInfo[CMDType]['commmand']
        TrueCmdBytesArray = EasyCMDL.GetHexCommand(TrueCmdList)
        CmdErrindex = []

        for x in range(len(cmd)):
            if cmd[x]!=TrueCmdBytesArray[x]:
                CmdErrindex.append(x)
        if len(CmdErrindex)==0:
            print(CMDType+' Success')
            return CMDType
        else:
            print(CmdErrindex)

    else:
        print('{}:Hard Mode'.format(CMDType))

def BasicReturnCodeFuc(CMDType):
    D=0xff
    S=0x02
    ReturnData=[]
    APDU_OK=[0x90,0x00]

    if CMDType=='PLC Reboot':
        ReturnData=APDU_OK

    elif CMDType=='PLC Firmware Version':

        MachineTypeName = 'PLA'
        MachineVerInfo=[]
        for x in MachineTypeName:
            MachineVerInfo.append(ord(x))

        MachineVersion = [0x20,0x19,0x01,0x09,0x00]

        for x in MachineVersion:
            MachineVerInfo.append(x)

        for x in APDU_OK:
            MachineVerInfo.append(x)

        ReturnData=MachineVerInfo

    elif CMDType=='Flap Action':
        ReturnData = APDU_OK

    elif CMDType=='Flap Position':
        GateStatusDict={'OPENA':0x00,'OPENB':0x01,'CLOSE':0x02,'MOVING':0x03,'UNKNOW':0x04}
        GateStatusList=[]
        GateStatusList.append(GateStatusDict['UNKNOW'])
        for x in APDU_OK:
            GateStatusList.append(x)
        ReturnData = GateStatusList

    elif CMDType=='Flap Position':
        ReturnData = APDU_OK

    elif CMDType=='Set Direction Mode':
        ReturnData = APDU_OK

    elif CMDType=='Set Parameters':
        ReturnData = APDU_OK


#-------------------------------------------------------------------------------
    ReturnCodeLen=len(ReturnData)
    ReturnCodeList=[]

    ReturnCodeList.append(D)
    ReturnCodeList.append(S)
    ReturnCodeList.append(ReturnCodeLen)
    for x in ReturnData:
        ReturnCodeList.append(x)

    EDC=0
    for x in ReturnCodeList:
        EDC^=x
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
