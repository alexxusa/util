import argparse
from multiprocessing import Process
import os
import socket
import subprocess
import sys
import time
import psutil

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_app(env, command, port):
    print(command)    
    subprocess.run(f'{command} & /kaggle/working/zrok/zrok share public http://localhost:{port} --headless', shell=True, env=env)


def find_and_terminate_process(port):
    for process in psutil.process_iter(['pid', 'name', 'connections']):
        for conn in process.info.get('connections', []):
            if conn.laddr.port == port:
                print(f"Port {port} is in use by process {process.info['name']} (PID {process.info['pid']})")
                try:
                    process.terminate()
                    print(f"Terminated process with PID {process.info['pid']}")
                except psutil.NoSuchProcess:
                    print(f"Process with PID {process.info['pid']} not found")

def main():
    parser = argparse.ArgumentParser(description='Start Zrok with shell command and port')
    parser.add_argument('--command', help='Specify the command to run with Zrok')
    parser.add_argument('--port', help='Specify the port')
    args = parser.parse_args()
    
    print(args.port)
    print(args.command)
    env = os.environ.copy()
    target_port = args.port
    command = args.command
    if is_port_in_use(int(target_port)):
        find_and_terminate_process(int(target_port))
    else:
        print(f"Port {target_port} is free.")
    
    open('log.txt', 'w').close()
    
    p_app = Process(target=run_app, args=(env, command, target_port,))
 
    
    p_app.start() 
    p_app.join()
 
    
if __name__ == '__main__':

    main()

