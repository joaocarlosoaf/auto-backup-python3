# auto-backup-python3
Automatic backup python3

Script para fazer backup automático do servidor A para servidor B usando python3.
Todo o processo é relatado no log no servidor A, log no servidor B, e envia o log por email (caso não queria, só comendar a função 'sendNotifyEmail' na linha 105)  

Pre requisitos:

* Executar o SSH pelo menos uma vez na maquina para gerar os arquivos knows_hosts (evitando o erro "not found in known_hosts")
* Criar as pastas que serão usadas antes de executar o script
* pip3 install email
* pip3 install smtplib
* pip3 install sh
* pip3 install scp
* pip3 install paramiko

E setar as variaveis de configuração:

## Usuário do sistema
_user_so = ''

## Hora da scheduler
_time_scheduler = ''

## log file
_path_log = '/home/' + _user_so + '/bkp/'

## Parâmetros do Banco 
_bd_file_bkp = ''
_bd_path_file_bkp = '/home/' + _user_so + '/bkp/'
_bd_host =  '127.0.0.1'
_bd_database = ''
_bd_user = ''

## SCP parametros
_scp_host = '
_scp_port = ''
_scp_user = ''
_scp_pssw = ''
_scp_path = ''

## Configuração SMTP
_smpt_server = ''
_smtp_email = ''
_smtp_pssw = ''
_smtp_port = 587
_smtp_to_email = ''
_smpt_tittle_email = 'Backup Log'
