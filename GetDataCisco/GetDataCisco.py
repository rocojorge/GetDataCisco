# 2022 Gabriel Melero - gabrix177@hotmail.com - Gencom S.R.L 
#Programma che analizza l'output dato da Paramiko e crea le comode cartelle e file, questi sono quelli nell'elenco dei comandi.
# Il modo per connettersi sara tramite SSH al router Cisco e ti invieremo i comandi per memorizzare le tue risposte, 
# che verranno elaborate e archiviate. Otterremo dall'ambiente le variabili necessarie per connetterci e creare i percorsi delle cartelle.
# error = 2, human error, code or input.
# error = 1, internal error, the function crash.

import paramiko,time,os,re,getpass,shutil
import IFX_SCONF

firstDir = '/tmp'
ifx_sconf = IFX_SCONF.IFX_SCONF()

def ConnectToTheDevice(hostname,username,password):
    try:
        cliente = paramiko.SSHClient()  #1
        cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #2
        cliente.connect(hostname=hostname, #IFX_SCONF_DEVICE_ADDRESS
                        username=username, #IFX_SCONF_DEVICE_USERNAME
                        password=password, #IFX_SCONF_DEVICE_PASSWORD
                        auth_timeout=25) #3
        #SCP line right here, I have to check
        session = cliente.invoke_shell() #4
        session.settimeout(timeout=20) #Impostazione di un timeout se le cose si complicano troppo
        error = None
    except paramiko.AuthenticationException as error_paramiko:
            print(error_paramiko)
            error=1
            return error_paramiko,error
    except paramiko.SSHException as error_paramiko:
            print(error_paramiko)
            error=1
            return error_paramiko,error
    except:
            print('Error Desconocido')
            error=1
            return 'Error Desconocido',error

    return session,None #

def TakeUserHostName(session):
    error_value = 1
    try:
        session.send('echo $HOSTNAME\n')
        time.sleep(.1)
        output = session.recv(65000).decode()
        outlines = output.splitlines()
        outlines.pop()
        outlines.reverse()
        outlines.pop()
        HOSTNAME = outlines[0]
        session.send('echo $USER\n')
        time.sleep(.1)
        output = session.recv(65000).decode()
        outlines1 = output.splitlines()
        outlines1.pop()
        outlines1.reverse()
        outlines1.pop()
        USER = outlines1[0]
        if USER==HOSTNAME:
            for i in range(3):
                session.send('\n')
                time.sleep(.1)
                output = session.recv(65000).decode()
            output_inlist = output.splitlines()
            lenght_list = len(output_inlist)
            line_to_use = output_inlist[1]
            final_form_use = line_to_use.split('-',1)
            USER = final_form_use[0]
            HOSTNAME = final_form_use[1]
    except:
        print('Can not take the USER and HOST name')
        return error_value, error_value

    USER = re.escape(USER)
    HOSTNAME = re.escape(HOSTNAME)
    return USER,HOSTNAME

def check_root(session):
    yroot=False
    try:
        # = Cisco Switches root symbol
        session.send("\n")
        time.sleep(.5)
        output1=str(session.recv(65000).decode())
        longth=len(output1)
        numero=output1.find("#",(longth-5),longth)
        if numero!=int("-1"):
            return True
        else:
            return yroot
    except:
        print('Problem with the connection')
        return 0

def auth_as_root(session,passwd):
    try:
        commandoSU = "enable\n"
        session.send(commandoSU+"\n")
        time.sleep(.5)
        session.send(passwd+"\n")
        time.sleep(.5)
        output=str(session.recv(65000).decode())
        if not check_root(session):
            return 1
        return None
    except:
        print('Problem with the loggin, the password have to be an string')
        return 2

def RunCommand(session,out,HOSTNAME,USER,command):
    try:
        outputlist=[]
        if out==0:
            out=1
        session.send('term length 0\n')
        time.sleep(.1)
        output = session.recv(65000*out).decode(encoding='cp850')
        session.send(command+'\n')
        listo = session.recv_ready()
        num=2
        listo = False
        while not listo:
            time.sleep(num)
            listo = session.recv_ready()
            if listo:
                output = session.recv(65000*out).decode(encoding='cp850')
            if num>=20:
                outputlist = None
                num = None
                break
            outputstr = str(output)
            outputlist.append(outputstr)
            #while not re.search('\[['+USER+']*.'+HOSTNAME+' ~\]\$', outputstr) and listo:# LINUX VERSION
            while not re.search(''+USER+'*.'+HOSTNAME, outputstr) and listo: #CISCO ROUTERS VERSION
                out +=2
                output = session.recv(65000*out).decode(encoding='cp850')
                time.sleep(0.1)
                outputstr = str(output)
                outputlist.append(outputstr)
                listo = session.recv_ready()
           # if re.search('\[['+USER+']*.'+HOSTNAME+' ~\]\$', outputstr): #LinuxVersion
            if re.search('['+USER+']*.'+HOSTNAME, outputstr):
                listo = True
            num+=1
            out+=2
        return outputlist,num
    except shutil.Error as error:
        print('Fatal error')
        return None,None

def CleanFileGeneral(final_output, times_executed, HOSTNAME, USER ):
    if final_output == times_executed:
        return 1
    archivio = ''
    for line in final_output:
        archivio += line
    archivio = str( archivio )
    archivio = re.sub(r"\r", "", archivio )
    archivio = re.sub(r'[\n]*'+'['+USER+']*.'+HOSTNAME,"", archivio)
    archivio = re.sub('^\s','', archivio)
    archivio = re.sub('\n\s+','\n', archivio)
    archivio = re.sub('\n+','\n', archivio)
    archivio = re.sub('\n+$','', archivio )
    return archivio

def RunningData(session, out_number, HOSTNAME, USER, command):
    ruta = os.path.join(firstDir, ifx_sconf.get_group(), ifx_sconf.get_Branch(), ifx_sconf.get_Device_Sysname() )
    final_output, times_executed = RunCommand( session, out_number, HOSTNAME, USER, command )
    archivio = CleanFileGeneral(final_output, times_executed, HOSTNAME, USER )
    archivio = re.sub(command+'\n*',"", archivio)
    return archivio, ruta

def CreateDir():
    try:
        ruta = os.path.join(firstDir, ifx_sconf.get_group() , ifx_sconf.get_Branch(), ifx_sconf.get_Device_Sysname() )
        os.rmdir(ruta)
    except:
        try:
            ruta = os.path.join(firstDir, ifx_sconf.get_group() , ifx_sconf.get_Branch(), ifx_sconf.get_Device_Sysname())
            shutil.rmtree(ruta)
        except:
            try:
                ruta = os.path.join(firstDir, ifx_sconf.get_group() , ifx_sconf.get_Branch(), ifx_sconf.get_Device_Sysname())
                os.makedirs(ruta)
                return ruta, None
            except:
                print('Error from os')
                error = 1
                return 'Error from os', error
    try:
        ruta = os.path.join(firstDir, ifx_sconf.get_group() , ifx_sconf.get_Branch(), ifx_sconf.get_Device_Sysname())
        os.makedirs(ruta)
        return ruta, None
    except:
        print('Error from os')
        error = 1
        return 'Error from os', error


def CreateFile(file_name, ruta_file):
    with open(ruta_file,'w') as archivo: archivo.write(file_name) #Questo ï¿½ per creare i file, ma, non lo useremo, solo per te per sapere di cosa si tratta

def main():
    out_number = 5
    error = None
    commands = ("show running-config","show vlan", "show version", "show inventory"
            ,"show license", "show env all", "show vtp status", "show vtp password"
            , "show interface status", "show cdp neigh det") #Python Tupla, It is ordered and cannot change.
    session,error1 = ConnectToTheDevice( ifx_sconf.get_Device_Address(), ifx_sconf.get_Device_Username(), ifx_sconf.get_Device_Password() )
    if not check_root(session):
        passwd = getpass.getpass('Root Password: ')
        error2 = auth_as_root(session,passwd)
    else:
        error2 = None
    ruta,error3 = CreateDir()
    if error or error1 or error2 or error3 : #revisar en el futuro
        print(error1,'\n',error2,'\n',error3,'\n')
    else:
        USER,HOSTNAME = TakeUserHostName( session )
        if USER != HOSTNAME:
            for command in commands:
                if command =='show running-config':
                   archivio,ruta = RunningData(session, out_number, HOSTNAME, USER, command)
                   archivio = re.sub(r'show running-config\nBuilding configuration...\n\nCurrent configuration : [0-9]+ bytes\n',"", archivio )
                   ruta = os.path.join(ruta,'running-config.conf')
                   with open(ruta,'w') as archivo: archivo.write( archivio )

                if command =='show vlan':
                    #VLAN
                   archivio,ruta = RunningData(session, out_number, HOSTNAME, USER, command)
                   archivio = re.sub(r'show vlan\n\n','', archivio )
                   ruta = os.path.join(ruta,'info-vlan.txt')
                   with open(ruta,'w') as archivo: archivo.write( archivio )
                   #Create the vlan.conf
                   ruta = os.path.join(firstDir, ifx_sconf.get_group() , ifx_sconf.get_Branch(), ifx_sconf.get_Device_Sysname() )
                   partA = archivio[:archivio.find('VLAN Type')-1].splitlines()
                   indexdel=[]
                   espacio1 = 0
                   espacio2 = 0
                   for j in range(len(partA)):
                      if re.search('^ +(Gi[0-9]/[0-9]/[\d],?)+',partA[j]):
                           indexdel.append(partA[j])
                      if re.search("-+ -+ -+ -+",partA[j]):
                           j = partA[j].split(' ')
                           espacio1 = len(j[0])
                           espacio2 = len(j[1])
                   for j in indexdel:
                        partA.remove(j)
                   ArraydA = []
                   for j in partA:
                       ArraydA.append(((j[:espacio1]).strip(),(j[espacio1+1:espacio2+espacio1+1]).strip()))
                   ArraydA.pop(0)
                   ArraydA.pop(0)
                   borrarA =[]
                   for j in ArraydA:
                       if re.search('^100[0-5]',j[0]) or re.search('^1$',j[0]):
                          borrarA.append(j)
                   for j in borrarA:
                       ArraydA.remove(j)
                   archivio = ''
                   for j in ArraydA:
                       archivio+='VLAN '+j[0]+'\n'+'  NAME '+j[1]+'\n\n'
                   ruta = os.path.join(ruta,'vlan.conf')
                   with open(ruta,'w') as archivo:archivo.write(archivio)

                if command =='show version':
                   #show version 
                   archivio,ruta = RunningData(session, out_number, HOSTNAME, USER, command)
                   archivio = re.sub(r'show version\n',"", archivio)
                   ruta = os.path.join(ruta,'info-version.txt')
                   with open(ruta,'w') as archivo: archivo.write( archivio )

                if command =='show inventory':
                   archivio,ruta = RunningData(session, out_number, HOSTNAME, USER, command)
                   archivio = re.sub(r'show inventory\n',"", archivio )
                   ruta = os.path.join( ruta, 'info-inventory.txt')


                if command =='show license':
                   archivio,ruta = RunningData(session, out_number, HOSTNAME, USER, command)
                   archivio = re.sub(r'show license\n',"", archivio )
                   ruta = os.path.join(ruta, 'info-license.txt')
                   with open(ruta,'w') as archivo: archivo.write( archivio )

                if command =='show env all':
                   archivio,ruta = RunningData(session, out_number, HOSTNAME, USER, command)
                   archivio = re.sub(r'show env all\n',"", archivio )
                   ruta = os.path.join(ruta, 'info-environment.txt')
                   with open(ruta, 'w') as archivo: archivo.write( archivio )

                if command=='show vtp status':
                   archivio,ruta = RunningData(session, out_number, HOSTNAME, USER, command)
                   archivio = re.sub(r'show vtp status\n',"", archivio )
                   ruta = os.path.join(ruta, 'info-vtp_status.txt')
                   with open(ruta, 'w') as archivo: archivo.write( archivio )

                if command=='show vtp password':
                   archivio,ruta = RunningData(session, out_number, HOSTNAME, USER, command)
                   archivio = re.sub(r'show vtp password\n',"", archivio )
                   ruta = os.path.join(ruta, 'info-vtp_password.txt')
                   with open(ruta, 'w') as archivo: archivo.write( archivio )

                if command =='show interface status':
                   archivio,ruta = RunningData(session, out_number, HOSTNAME, USER, command)
                   archivio = re.sub(r'show interface status\n\n',"", archivio)
                   ruta = os.path.join(ruta, 'info-interface-status.txt')
                   with open(ruta, 'w') as archivo: archivo.write( archivio )

                if command =='show cdp neigh det':
                   archivio,ruta = RunningData(session, out_number, HOSTNAME, USER, command)
                   archivio = re.sub(r'show cdp neigh det\n',"", archivio )
                   ruta = os.path.join(ruta, 'info-cdp.txt')
                   with open(ruta, 'w') as archivo: archivo.write( archivio )
    session.close()
                  
if __name__ == '__main__':
    main()