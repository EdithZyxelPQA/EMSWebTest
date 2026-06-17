import requests
import urllib
import zipfile
import shutil
import subprocess
import re
import os
import datetime

CurrentPath = os.getcwd()
info_file = f"{CurrentPath}\\chromedriver_info.txt"

# init
open(info_file,"w+")
print("\n" + str(datetime.datetime.now()).split(":")[0],file = open(info_file, '+a'))
wfile = open(info_file,"a+")
chromedriver_txt_file_path = CurrentPath
chromedriver_folder = CurrentPath
# with open(f"{chromedriver_txt_file_path}chromedriver.txt", "w") as file:
#     file.write('')
#     pass
# chromedriver_txt_file_path += 'chromedriver.txt'
chromedriver_txt_file_path = info_file
executable_chromedriver_path = f"{chromedriver_folder}chromedriver.exe"
def my_get_current_chrome_version():
    try:
        command = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        output = result.stdout

        match =  re.search(r'version\s+REG_SZ\s+([\d.]+)', output)
        if match:
            return match.group(1)
        else:
            return None
    except Exception as e:
        print(f"Error occurred: {e}")

def Update_Chromedriver3(chromedriver_folder): 

    print("Update_Chromedriver3 start - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - ",file = open(info_file, '+a'))   
    if_chromdriver_fail = False
    if_fail = False

    # [ Get chromedriver download version from local current chrome version ] 
    current_chrome_ver_from_err = ''
    error_msg = ''
    if_chromdriver_fail = True
    current_chrome_ver_from_err = str(my_get_current_chrome_version())
    
    if if_chromdriver_fail:
        # remove part of version number 127.0.6533.89 -> 127.0.6533
        tmp_dot_ls = current_chrome_ver_from_err.split('.')
        current_chrome_ver_from_err = tmp_dot_ls[0] + '.' + tmp_dot_ls[1] + '.' + tmp_dot_ls[2]
        
        # parse specific version chromdriver-win64 dowload url (get latest one)
        response = requests.get("https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json")
        response.raise_for_status()
        data = response.json()
        specific_version = current_chrome_ver_from_err
        specific_version_url = None
        for entry in data['versions']:
            entry_version = entry['version'].split('.')[0] + '.' + entry['version'].split('.')[1] + '.' + entry['version'].split('.')[2]
            if entry_version == specific_version:
                specific_version_url = entry['downloads']['chromedriver'][4]['url']
                print(entry_version, specific_version, specific_version_url)
                print(entry_version, specific_version, specific_version_url, file = open(info_file, '+a'))
        download_url = specific_version_url
        print("\nDownload url:",download_url, file = open(info_file, '+a'))

        # download to D:/
        print("Chrome version is not match with driver version, download another one.",file = open(info_file, '+a'))   
        save_path = f"D:/chromedriver.zip"
        urllib.request.urlretrieve(download_url, save_path)
        unzip_path = "D:/"
        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        shutil.copy('D:/chromedriver-win64/chromedriver.exe', chromedriver_folder)
        print("\Download done.", file = open(info_file, '+a'))

        # f_version = open(chromedriver_txt_file_path, 'w', encoding='utf8')
        # f_version.write(download_url)
        # f_version.close()
    elif if_fail == False:
        print('\nchromedriver work success\n', file = open(info_file, '+a'))
    else:
        # error
        print('error msg:',error_msg, file = open(info_file, '+a'))
        raise Exception(error_msg)
    print("Update_Chromedriver3 finished - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - \n",file = open(info_file, '+a'))   



def Update_Chromedriver(chromedriver_txt_file_path, chromedriver_folder):


    # Get chrome version
    try:
        import chrome_version

    except:
        print("Need install chrome_version module",file = open(info_file, '+a'))
        return

    # Get Chrome version
    chrome_ver = chrome_version.get_chrome_version()
    print("Chrome version:" + chrome_ver,file = open(info_file, '+a'))
    lst_chrome_ver = chrome_ver.split('.')
    chrome_ver_main = lst_chrome_ver[0]
    # my current chrome ver
    my_chrome_ver = my_get_current_chrome_version() # .split('.')[0]
    if chrome_ver_main != my_chrome_ver.split('.')[0]:
        print(f"(My Current Chrome version: {my_chrome_ver} , may need update chrome browser)",file = open(info_file, '+a'))

    # Get Chrome driver version
    lineNum = 0
    driver_ver = ""
    f_ver = open(chromedriver_txt_file_path, 'r', encoding='utf8')
    for line in iter(f_ver):
        lineNum=lineNum+1
        if lineNum == 1:
            driver_ver = line.strip()
            break    

    print("Driver version:" + driver_ver,file = open(info_file, '+a'))
    lst_driver_ver = driver_ver.split('.')
    driver_ver_main = lst_driver_ver[0]

    if chrome_ver_main != driver_ver_main: 
        print("Chrome version is not match with driver version",file = open(info_file, '+a'))

        # Download new chromedriver
        url = "https://googlechromelabs.github.io/chrome-for-testing/"
        response = requests.get(url)
        source = response.text

        mk1 = source.find('<h2>Stable</h2><p>Version:')
        mk2 = source.find('<code>', mk1)
        mk3 = source.find('</code>', mk2)
        stable_version = source[mk2+6:mk3]
        print("Stable version:" + stable_version,file = open(info_file, '+a'))

        download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{stable_version}/win64/chromedriver-win64.zip"
        save_path = f"D:/chromedriver.zip"
        urllib.request.urlretrieve(download_url, save_path)

        unzip_path = "D:/"
        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

        # shutil.copy('D:/chromedriver-win64/chromedriver.exe', chromedriver_folder)
        shutil.copy('D:/chromedriver-win64/chromedriver.exe', os.getcwd())

        # f_version = open(chromedriver_txt_file_path, 'w', encoding='utf8')
        # f_version.write(stable_version)
        # f_version.close()
        with open(chromedriver_txt_file_path, 'r+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(stable_version + "\n" + content)
            f.close()
            

    print("drivers done")


try:
    # Update_Chromedriver(chromedriver_txt_file_path, chromedriver_folder)
    Update_Chromedriver3(chromedriver_folder)
    print(f'Update Chromedriver Done.',file = open(info_file, '+a'))
except Exception as e:
    print(f'Update Chromedriver Something error: {e}',file = open(info_file, '+a'))


wfile.close()