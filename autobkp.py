import time
import gzip
import threading
import subprocess
from sh import pg_dump
from paramiko import SSHClient
from scp import SCPClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

## Usuário do sistema que execurata o serviço
_user_so = 'backup'

## Hora da scheduler
_time_scheduler = '00:00'

## log file
_path_log = '/home/' + _user_so + '/bkp-service/'

## Parâmetros do Banco 
_bd_file_bkp = ''
_bd_path_file_bkp = '/home/' + _user_so + '/bkp-service/'
_bd_host =  '127.0.0.1'
_bd_database = ''
_bd_user = ''

## SCP parametros
_scp_host = ''
_scp_port = ''
_scp_user = ''
_scp_pssw = ''
_scp_path = ''

## Configuração SMTP
_smpt_server = 'smtp.gmail.com'
_smtp_email = ''
_smtp_pssw = ''
_smtp_port = 587
_smtp_to_email = ''
_smpt_tittle_email = ''

def saveLog(menssage_):
    log = open(_path_log + time.strftime("%Y%m%d") + _bd_file_bkp + '.log', 'a')
    log.write(time.strftime("[%Y%m%d%H:%M:%S] --> ") + menssage_ +'\n')
    log.close()

def execCmdBash(cmd_):
    return subprocess.getoutput(cmd_)

def createSshToCopy():
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(_scp_host, _scp_port, _scp_user, _scp_pssw)
    scp = SCPClient(ssh.get_transport())
    scp.put(_bd_path_file_bkp, recursive=True, remote_path=_scp_path)
    scp.close()

def sendNotifyEmail(context_email):

    server = smtplib.SMTP(_smpt_server, _smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(_smtp_email, _smtp_pssw)

    msg = MIMEMultipart()
    msg['From'] = _smtp_email
    msg['To'] = _smtp_to_email
    msg['Subject'] = _smpt_tittle_email
    msg.attach(MIMEText(context_email, 'plain'))

    server.sendmail(_smtp_email, _smtp_to_email, msg.as_string())
    server.quit()

def startBackup():

    saveLog('Start process backup')
        
    try:

        # Create backup file
        with gzip.open(_bd_path_file_bkp + _bd_file_bkp + '.gz', 'wb') as f:
            pg_dump('-h', _bd_host, '-U', _bd_user, _bd_database, _out=f)
        saveLog('File backup create')

        # Generate MD5 of file
        md5_value_file = execCmdBash('md5sum ' + _bd_path_file_bkp + _bd_file_bkp + '.gz')
        saveLog('md5 file backup -> ' + md5_value_file)

        # Copy backup with SCP
        createSshToCopy()
        saveLog('Copy file bkp is complete')

        # Copy log with SCP
        createSshToCopy()
        saveLog('Copy file log is complete')

        # Remove backup local
        execCmdBash('rm ' + _bd_path_file_bkp + _bd_file_bkp + '.gz')
        saveLog('Remove temp backup file')

        # Send email notification
        context_email = execCmdBash('cat ' + _path_log + time.strftime("%Y%m%d") + _bd_file_bkp + '.log')
        sendNotifyEmail(context_email)
        saveLog('Send notification email')

        # Backup Complete
        saveLog('Backup complete!')
        saveLog('File -> ' + _bd_file_bkp)

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        saveLog(message)

while True:
    if  time.strftime("%H:%M") == _time_scheduler:
            t1 = threading.Thread(name='uServiceStartBackup', target=startBackup)
            t1.start()
            time.sleep(120)

