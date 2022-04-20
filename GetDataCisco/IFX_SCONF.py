# 2022 Gabriel Melero - gabrix177@hotmail.com - Gencom S.R.L
import os

class IFX_SCONF:
    try:
        IFX_SCONF_GIT_GROUP = os.environ['IFX_SCONF_GIT_GROUP']
        IFX_SCONF_DEVICE_USERNAME = os.environ['IFX_SCONF_DEVICE_USERNAME']
        IFX_SCONF_DEVICE_SYSNAME = os.environ['IFX_SCONF_DEVICE_SYSNAME']
        IFX_SCONF_MONITOR_NAME = os.environ['IFX_SCONF_MONITOR_NAME']
        IFX_SCONF_BRANCH = IFX_SCONF_MONITOR_NAME.split(".")[2]
        IFX_SCONF_DEVICE_PASSWORD = os.environ['IFX_SCONF_DEVICE_PASSWORD']
        IFX_SCONF_DEVICE_ADDRESS = os.environ['IFX_SCONF_DEVICE_ADDRESS']
    except:
        IFX_SCONF_GIT_GROUP = 'IFX_SCONF_GIT_GROUP'
        IFX_SCONF_DEVICE_USERNAME = 'IFX_SCONF_DEVICE_USERNAME'
        IFX_SCONF_DEVICE_SYSNAME = 'IFX_SCONF_DEVICE_SYSNAME'
        IFX_SCONF_MONITOR_NAME = 'IFX_SCONF_MONITOR_NAME'
        IFX_SCONF_BRANCH = IFX_SCONF_MONITOR_NAME.split(".")[2]
        IFX_SCONF_DEVICE_PASSWORD = 'IFX_SCONF_DEVICE_PASSWORD'
        IFX_SCONF_DEVICE_ADDRESS = 'IFX_SCONF_DEVICE_ADDRESS'

    def __init__(self) -> None: 
        self.IFX_SCONF_GIT_GROUP = IFX_SCONF.IFX_SCONF_GIT_GROUP
        self.IFX_SCONF_DEVICE_USERNAME = IFX_SCONF.IFX_SCONF_DEVICE_USERNAME
        self.IFX_SCONF_DEVICE_SYSNAME = IFX_SCONF.IFX_SCONF_DEVICE_SYSNAME
        self.IFX_SCONF_MONITOR_NAME = IFX_SCONF.IFX_SCONF_MONITOR_NAME
        self.IFX_SCONF_BRANCH = IFX_SCONF.IFX_SCONF_BRANCH
        self.IFX_SCONF_DEVICE_PASSWORD = IFX_SCONF.IFX_SCONF_DEVICE_PASSWORD
        self.IFX_SCONF_DEVICE_ADDRESS = IFX_SCONF.IFX_SCONF_DEVICE_ADDRESS

    def get_group(self):
        return self.IFX_SCONF_GIT_GROUP

    def get_Device_Username(self):
        return self.IFX_SCONF_DEVICE_USERNAME

    def get_Device_Sysname(self):
        return self.IFX_SCONF_DEVICE_SYSNAME

    def get_Monitor_Name(self):
        return self.IFX_SCONF_MONITOR_NAME

    def get_Branch(self):
        return self.IFX_SCONF_BRANCH

    def get_Device_Password(self):
        return self.IFX_SCONF_DEVICE_PASSWORD

    def get_Device_Address(self):
        return self.IFX_SCONF_DEVICE_ADDRESS