#!/usr/bin/python3

import paramiko
import subprocess


def main():
    filename='ip_user_passwd.csv'
    fh=open(filename)    
    for line in fh:
        ip,user,passwd=line.split(',')
        passwd=passwd.rstrip()
        print(type(ip))
        dir_output=ssh_connection(ip, user, passwd, 'ls/var/www')
        hostname_output=ssh_connection(ip, user, passwd, 'hostname')
        print("this is my current ip")
        print(ip)         
        output_file(ip.encode() +b'\n')     
        if dir_output:
            print("This is what is in my www directory")
            output_file(dir_output)
        else:
            print("The www directory is empty")
            output_file(b'empty directory \n')
        output_file(hostname_output)
    fh.close()
    return

def output_file(ssh_connect):
    output='output.txt'
    f= open(output, "a")
    f.write("Output from ssh " + ssh_connect.decode())
    f.close()
    return


def ssh_connection(ip,user,passwd, command):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        ssh_output=ssh_session.recv(1024)
        print(ssh_output)
    return ssh_output



main()
