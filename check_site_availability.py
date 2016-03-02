from datetime import datetime
from os.path import expanduser, exists, isfile
from os import mkdir, chdir, system
from urllib.request import urlopen
from urllib.error import HTTPError

site = ''

folder_name_for_site = site[ site.find('//')+2 : ].replace('/','_') # change it to string with your name if needed

# this is a variable for sending email with error via your exe file without log file which adds automatically.
cli_command = r''

now = datetime.now()
date = str(datetime.date(now))
time = str(datetime.time(now))
time = time[ : time.find('.') ]

def add_data(new_data):
    data = open(data_file, 'a')
    data.write(new_data)
    data.close()
def send_email_on_error(cli_command):
    system(cli_command + ' ' + data_file)

# Create directory and text file for automation if not exists
home_dir = expanduser(r'~') 
# home_dir = r'C:\tranzit' # Replace this variable with directory (string) where you want to keep logs if needed
base_automation_dir = home_dir + '\\automated_loging_system\\'
automation_dir = base_automation_dir + folder_name_for_site + '\\'
if not exists( home_dir ): mkdir( home_dir )
if not exists( base_automation_dir ): mkdir( base_automation_dir )
if not exists( automation_dir ): mkdir( automation_dir )
chdir(automation_dir)
data_file = automation_dir + '\\' + date + '.txt'

try:
    code = urlopen(site).getcode()
    if code == 200:
        new_data = time + ' - ' + str(code) + ' - ' + 'OK\n'
        add_data(new_data)
        send_email_on_error(cli_command)
    else:
        new_data = time + ' - ' + str(code) + ' - ' + 'partial success\n'
        add_data(new_data)
        exit()
except HTTPError as err:
    new_data = time + ' - ' + str(err.code) + ' - ' + 'ERROR: SOMETHING IS WRONG\n'
    add_data(new_data)
    send_email_on_error(cli_command)
    exit()
except Exception:        
    new_data = time + ' ERROR: SITE URL MAY BE BROKEN ! ! !\n'
    add_data(new_data)
    send_email_on_error(cli_command)

exit()