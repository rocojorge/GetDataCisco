# 2022 Gabriel Melero - gabrix177@hotmail.com - Gencom S.R.L
#Programma che analizza l'output dato da Paramiko e crea le comode cartelle e file, questi sono quelli nell'elenco dei comandi.


import IFX_SCONF, GetDataCisco

ifx_sconf = IFX_SCONF.IFX_SCONF()
firstdir = '/tmp'

def main():
    out_number = 5
    error = None
    start_command = 'config paging disable'
    commands = ('show run-config commands', 'show run-config startup-commands',
                'show inventory', 'show ap inventory all', 'show ap summary all', 'show ap join stats summary all',
               'show license capacity', 'show certificate all', 'show interface summary',
               "show sysinfo")
    session, error = GetDataCisco.ConnectToTheDevice( ifx_sconf.get_Device_Address(), ifx_sconf.get_Device_Username(), ifx_sconf.get_Device_Password() )
    if error == 1:
        return session,error
    ruta,error = GetDataCisco.CreateDir()
    if error == 1:
        return ruta,error
    USER, HOSTNAME = GetDataCisco.TakeUserHostName( session )
    if USER == HOSTNAME :
        return USER
    #Shouldn't be unhandled errors
    session.send( start_command+'\n' )
    GetDataCisco.time.sleep(0.5)
    output = session.recv(65000)
    for command in commands:
        if command == 'show run-config commands':
            archivio, ruta = GetDataCisco.RunningData( session,out_number,HOSTNAME, USER, command )
            archivio = GetDataCisco.re.sub('rogue ap .+\n*','', archivio )
            ruta = GetDataCisco.os.path.join(ruta,'run-config_commands.conf')
            with open(ruta,'w') as archivo: archivo.write( archivio )
        if command == 'show run-config startup-commands':
            archivio, ruta = GetDataCisco.RunningData( session,out_number,HOSTNAME, USER, command )
            archivio = GetDataCisco.re.sub('Config generation may take some time ...\n', '', archivio )
            archivio = GetDataCisco.re.sub('# WLC Config .+\n*', "", archivio )
            first_Mark = archivio.find(' \n! \n! ')
            archivio = archivio[:first_Mark]+GetDataCisco.re.sub('\n! .+','',archivio[first_Mark:])
            archivio = archivio[:first_Mark]+GetDataCisco.re.sub('\n! ','',archivio[first_Mark:])
            ruta = GetDataCisco.os.path.join(ruta,'run-config_startup-commands.conf')
            with open(ruta,'w') as archivo: archivo.write( archivio )
        if command == 'show inventory':
            archivio, ruta = GetDataCisco.RunningData( session,out_number,HOSTNAME, USER, command )
            ruta = GetDataCisco.os.path.join(ruta,'info-inventory.txt')
            with open(ruta,'w') as archivo: archivo.write( archivio )
        if command == 'show ap inventory all':
            archivio, ruta = GetDataCisco.RunningData( session,out_number,HOSTNAME, USER, command )
            ruta = GetDataCisco.os.path.join(ruta,'info-ap_inventory_all.txt')
            with open(ruta,'w') as archivo: archivo.write( archivio )
        if command == 'show ap summary all':
            archivio, ruta = GetDataCisco.RunningData( session,out_number,HOSTNAME, USER, command )
            ruta = GetDataCisco.os.path.join(ruta,'info-ap_summary_all.txt')
            with open(ruta,'w') as archivo: archivo.write( archivio )
        if command == 'show ap join stats summary all':
            archivio, ruta = GetDataCisco.RunningData( session,out_number,HOSTNAME, USER, command )
            ruta = GetDataCisco.os.path.join(ruta,'info-ap_join_stats.txt')
            with open(ruta,'w') as archivo: archivo.write( archivio )
        if command == 'show license capacity':
            archivio, ruta = GetDataCisco.RunningData( session,out_number,HOSTNAME, USER, command )
            ruta = GetDataCisco.os.path.join(ruta,'info-license_capacity.txt')
            with open(ruta,'w') as archivo: archivo.write( archivio )
        if command == 'show certificate all':
            archivio, ruta = GetDataCisco.RunningData( session,out_number,HOSTNAME, USER, command )
            ruta = GetDataCisco.os.path.join(ruta,'info-certificates.txt')
            with open(ruta,'w') as archivo: archivo.write( archivio )
        if command == 'show interface summary':
            archivio, ruta = GetDataCisco.RunningData( session,out_number,HOSTNAME, USER, command )
            ruta = GetDataCisco.os.path.join(ruta,'info-interface_summary.txt')
            with open(ruta,'w') as archivo: archivo.write( archivio )
        if command == 'show sysinfo':
            archivio, ruta = GetDataCisco.RunningData( session,out_number,HOSTNAME, USER, command )
            archivio = GetDataCisco.re.sub('< System Up Time.+\n*', '', archivio )
            archivio = GetDataCisco.re.sub('< CPU Average Usage.+\n*','', archivio )
            archivio = GetDataCisco.re.sub('.+ Average Usage.+\n*','', archivio )
            ruta = GetDataCisco.os.path.join(ruta,'info-sysinfo.txt')
            with open(ruta,'w') as archivo: archivo.write( archivio )

    session.send('logout\n')
    GetDataCisco.time.sleep(0.5)
    output = session.recv(65000).decode("cp850")
    session.send('n')
    GetDataCisco.time.sleep(0.5)
    output = session.recv(65000).decode("cp850")
    session.close()




if __name__ == '__main__':
    main()
