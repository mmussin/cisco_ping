'''
Ping IP addresses listed in text file

ping.py 1.2.3.4 username password host_list ping_log
'''

__author__ = 'mmussin'

import requests
import paramiko
import time
import sys

def getClient(host_i, username, password):
    global client
    global remote_conn
    global output
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host_ip, username=username, password=password, timeout=5)
        remote_conn = client.invoke_shell()
        output = remote_conn.recv(1000)
    except paramiko.SSHException:
        client.close()
        print "Connection failed"
        sys.exit()

def getFileList(filename):
    try:
        f_in = open(filename,'r')
        list = [line for line in f_in.read().split('\n') if line.strip()]
        return list
    except IOError:
        sys.exit("The file does not exist")

def openFile(filename, mode):
    try:
        file = open(filename, mode)
    except IOError:
        sys.exit("The file does not exist")

def pingList(ipaddress_list):
    file_out = open(ping_log, "w")
    for ip in ipaddress_list:
        remote_conn.send("ping {0}\n".format(ip))
        time.sleep(1)
        output = remote_conn.recv(10000)
        print output
        file_out.write(output)

if __name__ == '__main__':
    host_i = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    host_list = sys.argv[4]
    ping_log = sys.argv[5]
    getClient()
    file_list = getFileList(host_list)
    print file_list
    pingList(file_list)
