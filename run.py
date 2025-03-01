#==========================================================
#                    CONFIGURATION

# Use Latest Stable Release / Use Latest Snapshot
UPDATE_TO_SNAPSHOT = True # True/False

# Number of minutes in between each update check
Check_Interval = 2 # int (min 2)

#==========================================================

try:
    import sys, os, time, shutil, psutil, hashlib, subprocess, requests, logging, signal
    from datetime import datetime
except:
    import subprocess, os, sys
    subprocess.call(sys.executable, '-m', 'pip', 'install', 'psutil')
    subprocess.call([sys.executable,sys.argv[0]])
    exit()

if not os.path.exists('Logs'):
    os.mkdir('Logs')
logging.basicConfig(filename='Logs\\Update.py.log',level=logging.INFO,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',)
def print_log(text):
    logging.info(text)
    print(text)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# retrieve version manifest
response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
data = response.json()

minecraft_ver = {True:data['latest']['snapshot'],False:data['latest']['release']}[UPDATE_TO_SNAPSHOT]

# Create dependency files if they don't exist
open('eula.txt','w').write('eula=true')

if not os.path.exists('minecraft_server.jar'):
    f = open('minecraft_server.jar', 'x')
    
if not os.path.exists('world'):
    os.makedirs('world')

# get checksum of running server
if os.path.exists('minecraft_server.jar'):
    sha = hashlib.sha1()
    f = open("minecraft_server.jar", 'rb')
    sha.update(f.read())
    cur_ver = sha.hexdigest()
else:
    cur_ver = ""

for version in data['versions']:
    if version['id'] == minecraft_ver:
        jsonlink = version['url']
        jar_data = requests.get(jsonlink).json()
        jar_sha = jar_data['downloads']['server']['sha1']
        
        if cur_ver != jar_sha:
            print('='*78)
            print_log('Update Found.')
            print()
            print_log('Your sha1 is ' + cur_ver + '. Latest version is ' + str(minecraft_ver) + " with sha1 of " + jar_sha)
            print('='*78)
            
            print_log('Updating server...')
            
            link = jar_data['downloads']['server']['url']
            print_log('Downloading minecraft_server.jar from ' + link + '...')
            response = requests.get(link)
            open('minecraft_server.jar', 'wb').write(response.content)
            print_log('Downloaded.')
            
            print_log('Backing up world...')

            if not os.path.exists('world_backups'):
                os.makedirs('world_backups')

            backupPath = os.path.join('world_backups', str(minecraft_ver) + '_' + datetime.now().isoformat().replace(':', '-'))
            shutil.copytree("world", backupPath)
            
            print_log('Backed up world.')
            
            print_log('Starting server...')
            logging.info('='*78)
    
        else:
            print("Server is already up to date.")
            print('Latest version is ' + str(minecraft_ver))
            time.sleep(5)
        break

p = subprocess.Popen(['java', '-Xms4096M', '-Xmx4096M', '-jar', 'minecraft_server.jar','nogui'])
start_time = time.time()

time.sleep({True:Check_Interval,False:2}[Check_Interval>1]*60)

for proc in psutil.process_iter(['pid', 'name', 'create_time']):
    try:
        pid, name, ctime = proc.info['pid'], proc.info['name'], start_time - proc.info['create_time']
        if name == 'java.exe' and abs(ctime) < 1:
            os.kill(pid, signal.SIGTERM)
            subprocess.call([sys.executable,sys.argv[0]])
            exit()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
