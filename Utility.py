import os
import csv

#快捷指令
class CMDlink():

    def GetCMDGroup(self):
        if len(os.listdir('./Commands')) != 0:
            CommandGroupList = os.listdir('./Commands')

            for x in range(1, len(CommandGroupList) + 1):
                print('{}.{}'.format(x, CommandGroupList[x - 1]))

        CmdLinkNumber = eval(input('選擇指令群組:'))
        CmdLinkName = CommandGroupList[CmdLinkNumber - 1]

        return CmdLinkName

    def GetCommands(self,FileName):
        with open(FileName, newline='') as csvfile:
            # 讀取 CSV 檔案內容
            rows = csv.reader(csvfile, delimiter=' ')
            # 以迴圈輸出每一列
            for row in rows:
                print(row)


    def CmdlinksIndo(self,CmdFileName):
        filepath = './Commands/{}'.format(CmdFileName)
        # 指令名稱,輸出類型,接收類型,指令
        CMDDict = {}
        CMDFile = open(filepath, encoding='utf8')

        for x in CMDFile.readlines():
            y = x.rstrip().split(',')  # 移除/n
            CMDName = y[0]
            CMDDict[CMDName] = {}
            CMDDict[CMDName]['SendType'] = y[1]
            CMDDict[CMDName]['ReciveType'] = y[2]

            for x in range(3):
                y.pop(0)

            CMDDict[CMDName]['commmand'] = y[0].split(' ')
        return CMDDict

    def GetHexCommand(self,CommandWords):

        HexCMD = bytearray()
        for x in CommandWords:
            base16INT = int(x, 16)
            HexCMD.append(base16INT)

        return HexCMD


if __name__ == '__main__':
    #取得指令群
    CMDL=CMDlink()
    CmdFileName=CMDL.GetCMDGroup()
    CmdlinksInfo=CMDL.CmdlinksInfo(CmdFileName)
    print(CmdlinksInfo)

