# -*- coding: utf-8 -*-
from mccLog import mccLog
from mailHelper import mailHelper
import os
import win32api

class executor(object):
    def __init__(self, commandDict, openDict):
        self.mccLog = mccLog()
        self.mailHelper = mailHelper()
        self.commandDict = commandDict
        self.openDict = openDict

    def execute(self, exe):
        subject = exe['subject']
        self.mccLog.mccWriteLog(u'开始处理命令')
        self.mailHelper.sendMail('pass', 'Slave')
        if subject in self.commandDict:
            self.mccLog.mccWriteLog(u'执行命令')
            try:
                command = self.commandDict['subject']
                os.system(command)
                self.mailHelper.sendMail('Success', 'Boss')
                self.mccLog.mccWriteLog(u'执行命令成功')
            except Exception, e:
                self.mccLog.mccError(u'执行命令失败' + str(e))
                self.mailHelper.sendMail('error', 'Boss', e)

        elif subject in self.openDict:
            self.mccLog.mccWriteLog(u'打开文件')
            try:
                openFile = self.openDict[subject]
                win32api.ShellExecute(0, 'open', openFile, '', '', 1)
                self.mailHelper.sendMail('Sucess', 'Boss')
                self.mccLog.mccWriteLog(u'打开文件成功')
            except Exception, e:
                self.mccLog.mccError(u'打开文件失败' + str(e))
                self.mailHelper.sendMail('error', 'Boss', e)
        elif subject[:7].lower() == 'sandbox':
            self.sandBox(subject[8:])
        else:
            self.mailHelper.sendMail('error', 'boss', 'no such command')

    def sandBox(self, code):
        name = code.split('$n$')[0]
        code = code.split('$n$')[1]
        codestr = '\n'.join(code.split('$c$'))
        codestr = codestr.replace('$', ' ')
        with open(name, 'a') as f:
            f.write(codestr)
        os.system('python' + name)