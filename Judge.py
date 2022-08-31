from Utility import CMDlink



def CheckCMDType(cmd):
    CMDTypeList = []
    f=open('KSGate_CommandTypeList.text')
    for x in f.readlines():
        CMDTypeList.append(x)

    CLA=3
    INS=4

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

    print(CMDType)
    return CMDType

def AdvenceCheck(cmd,CMDType):
    EasyCMDL=CMDlink()
    EasyCmdlinksInfo = EasyCMDL.CmdlinksInfo('EasyCmds.csv')
    EasyTypeList=[]
    for x in EasyCmdlinksInfo.keys():
        EasyTypeList.append(x)
    CheckType=EasyTypeList.index(CMDType)



    if CheckType!=-1:

        TrueCmdList = CmdlinksInfo[CMDType]['commmand']
        TrueCmdBytesArray = CMDL.GetHexCommand(TrueCmdList)
        CmdErrindex = []

        for x in range(len(cmd)):
            if cmd[x]!=TrueCmdBytesArray[x]:
                CmdErrindex.append(x)
        if len(CmdErrindex)==0:
            print()
        else:
            print(CmdErrindex)

    else:
        print('Hard Mode')






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
