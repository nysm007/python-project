import paramiko
import time, datetime
import os
from multiprocessing import Pool

Host = "1xx.xx.xx.xxx"
username = "yy"
password = "pass"
DIRTAR = "/data/tar" # remote target dir

DIR = "/data/source/" # source dir
REMAIN = -1000
TIME = 60*60*4
processNum = 8


def compare(x, y):
    try:
        stat_x = os.stat(DIR + "/" + x)
        stat_y = os.stat(DIR + "/" + y)
        if stat_x.st_ctime < stat_y.st_ctime:
            return -1
        elif stat_x.st_ctime > stat_y.st_ctime:
            return 1
        else:
            return 0
    except Exception as e:
        return 0


def move(f, directory):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(Host, port=22, username=username, password=password, allow_agent=False, look_for_keys=False) 
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    sftp.put("{}/{}".format(DIR, f), "{}/{}".format(directory, f))
    sftp.close()
    try:
        os.remove("{}/{}".format(DIR, f))
    except OSError as e:
        print("[Error] Error occurs when processing {}".format(f))
    print("[INFO] {} has been processed.".format(f))

i = 2
j = 0
while(1):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(Host, port=22, username=username, password=password, allow_agent=False, look_for_keys=False) 
    directory = DIRTAR.format(i)
    j += 1
    if j%4 == 0:
        i += 1
        ssh.exec_command("mkdir -p {}".format(directory))
    
    files = os.listdir(DIR)
    files.sort(compare)
    if len(files) > 2*REMAIN:
        waitlist = files[:REMAIN]
        flag = True
        if flag:
            pool = Pool(processNum)
            for ele in waitlist:
                pool.apply_async(move, args=(ele, directory,))
            pool.close()
            pool.join()
            print("[INFO] Batch #{} done, waiting for {} seconds...".format(i, TIME))
            print("[TIME] {}".format(str(datetime.datetime.now())))
            time.sleep(TIME)
        else:
            move(ssh, waitlist[1], directory)
    else:
        time.sleep(TIME)
