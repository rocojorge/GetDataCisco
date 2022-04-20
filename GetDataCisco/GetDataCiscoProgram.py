import GetDataCisco, time

import IFX_SCONF
ifx_sconf = IFX_SCONF.IFX_SCONF()
session, error = GetDataCisco.ConnectToTheDevice( ifx_sconf.get_Device_Address(), ifx_sconf.get_Device_Username(), ifx_sconf.get_Device_Password() )
firstDir = '/tmp'
out_number = 5
USER, HOSTNAME = GetDataCisco.TakeUserHostName( session )
print(USER)
print(HOSTNAME)
#def show run-config commands
command = 'show run-config commands'
archivio, ruta = GetDataCisco.RunningData(session, out_number, HOSTNAME, USER, command)



#def show run-config startup-commands
command = 'show run-config startup-commands'
session.send('config paging disable\n')
time.sleep(.1)
output = session.recv(65000).decode()

archivio, ruta = GetDataCisco.RunningData (session, out_number, HOSTNAME, USER, command)
archivio = GetDataCisco.re.sub(command+'\n*',"", archivio )
archivio = GetDataCisco.re.sub('[\n]*Config generation may take some time ...[\n]*',"", archivio )
archivio = GetDataCisco.re.sub('^[\n]*# WLC Config Begin.*[\n]*',"", archivio )
archivio = GetDataCisco.re.sub('[\n]*# WLC Config End .*$',"", archivio )





session.close()
print(session)
print(ruta)



