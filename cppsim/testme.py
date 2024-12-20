import os
import struct
from time import sleep
from datetime import datetime
from subprocess import run, Popen, PIPE

start = -1

def run_cpp_eval(vars):
    global start

    run('make')

    command = os.path.join('.', 'evaluator16')
    inp = bytes(vars)

    start = datetime.now()
    print('\n',start,'\n')
    print('\n',command,'\n')

    proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=False, text=False)
    print('python wrote:', proc.stdin.write(inp),'bytes\n')
    proc.stdin.flush()
    res, err = proc.communicate()
    print('stdout:', res, '\n')
    print('stderr:', err, '\n')
    
    try:
        mae = int.from_bytes(res[:8], byteorder='little')
        print('MAE:',mae,'\n')
    except:
        pass
        
    return 

############################################## Main ###############################################
if __name__ == '__main__':

    vars = [14 for i in range(201)] # 39 201 907 
    print(vars)
    run_cpp_eval(vars)

    print('time:', datetime.now() - start,'\n')
    print('testme done')
