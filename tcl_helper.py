import os
import shutil
from subprocess import Popen
from config import CWD, TOP_DIR, TEMP_DIR, SRC_DIR, OUT_DIR, MAIN_SCR, MAIN_RTL, ADDER_MAP, VAR_D, CLOCK

def create_files(name, main_src):
    """Creates files for Genus sythesis.
    Edits the main TCL script for import directories and output directories

        Args:
            name (str): the name of the individual, which is going to be simulated and syhtesized 

        Returns:
            new_dir (str): path to the temporary directory created
    """
    if(not os.path.exists(os.path.join(TOP_DIR, TEMP_DIR))):
            os.mkdir(os.path.join(TOP_DIR, TEMP_DIR))

    # copy files
    new_dir = os.path.join(TOP_DIR, TEMP_DIR, name)     # temporary dir path
    if os.path.exists(new_dir):                         # if it exists erase
        shutil.rmtree(new_dir)
    os.mkdir(new_dir)                                   # create temporary dir
    get_dir = os.path.join(CWD, TOP_DIR, SRC_DIR)       # get vhdl files from here
    src_dir = os.path.join(CWD, new_dir, SRC_DIR)       # put vhdl files here
    shutil.copytree(get_dir, src_dir)                   # copy files
    get_dir = os.path.join(CWD, TOP_DIR, main_src)      # get tcl script from here
    put_dir = os.path.join(CWD, new_dir)                # put tcl script from here
    shutil.copy(get_dir, put_dir)                       # copy files

    # edit main tcl script
    scr_dir = os.path.join(put_dir, main_src)           
    with open(scr_dir, 'r') as file:
        data = file.readlines()
        file.close()
    lib_dir = os.path.join(CWD, TOP_DIR) 
    out_dir = os.path.join(CWD, TOP_DIR, OUT_DIR) 
    for i,line in enumerate(data):
        if(line.startswith('set_db init_lib_search_path')):
            data[i] = 'set_db init_lib_search_path {' + lib_dir + '}  -quiet\n'
            continue
        elif(line.startswith('set_db init_hdl_search_path')):
            data[i] = 'set_db init_hdl_search_path {' + src_dir + '}  -quiet\n'
            continue
        elif(line.startswith('report_timing')):
            data[i] = 'report_timing > ' + out_dir + '/' + name + '_time.rpt\n'
            continue
        elif(line.startswith('report_power')):
            data[i] = 'report_power > ' + out_dir + '/' + name + '_power.rpt\n'
            continue
        elif(line.startswith('report_area')):
            data[i] = 'report_area > ' + out_dir + '/' + name + '_area.rpt\n'
            continue

    with open(scr_dir, 'w') as file:
        file.writelines( data )
        file.close()

    return new_dir

def build_rtl(name, vars, adder_map, main_rtl):
    """Builds the RTL description of the multiplier based on the vars passed as argument.

        Args:
            name (str): the name of the temporaty directory that contains the rtl files
            vars (list): specific adders to put at each location in the design

        Returns:
            None
    """
    # edit rtl file
    rtl_dir = os.path.join(CWD, TOP_DIR, TEMP_DIR, name, SRC_DIR, main_rtl)
    with open(rtl_dir, 'r') as file:
        data = file.readlines()
        file.close()
    for i,line in enumerate(data):
        try:
            j = adder_map.index(line[0:len(adder_map[0])])
        except:
            continue
        ports = line.index(' port')
        colon = line.index(' : ')
        data[i] = line[0:colon+3] + str(vars[j]) + line[ports:]
    with open(rtl_dir, 'w') as file:
        file.writelines( data )
        file.close()
    return

def run_tcl(name, out, main_src):
    """Runs the TCL script in the temporaty directory given as argument.

        Args:
            name (str): the name of the temporaty directory that contains the scipt
            out (bool): whether to print on stdout/stderr or not

        Returns:
            p (Popen): process created
    """

    # Delete stray files
    area_dir = os.path.join(TOP_DIR, OUT_DIR, name+'_area.rpt')
    if os.path.exists(area_dir):
        os.remove(area_dir)
    time_dir = os.path.join(TOP_DIR, OUT_DIR, name+'_time.rpt')
    if os.path.exists(time_dir):
        os.remove(time_dir)
    power_dir = os.path.join(TOP_DIR, OUT_DIR, name+'_power.rpt')
    if os.path.exists(power_dir):
        os.remove(power_dir)

    command = 'genus -f '+main_src+' -batch'
    if(not out):
        command += ' > /dev/null 2>&1'
    work_dir = os.path.join(CWD, TOP_DIR, TEMP_DIR, name)
    p = Popen(command, cwd = work_dir, shell=True)
    return p

def get_scores(name):
    """Reads Genus report values for an individual with given name from the tcl_out directory.

        Args:
            name (str): the name of the individual

        Returns:
            time (int): clock slack in picoseconds
            area (float): area in micrometers^2
            power (float): power consumption in milliwatts
    """

    area = -1
    time = -1
    power = -1

    # read area report
    area_dir = os.path.join(CWD, TOP_DIR, OUT_DIR, name + '_area.rpt')
    if os.path.exists(area_dir):
        with open(area_dir, 'r') as file:
            data = file.readlines()
            file.close()
        for i,line in enumerate(data):
            if(line.startswith('main')):
                line_lst = line.split(' ')[::-1]
                for item in line_lst:
                    try:
                        temp_flt = float(item)
                        area = temp_flt
                        break
                    except:
                        continue
                break
    if(area == -1):
        raise Exception('TCL_HELPER Error! Failed to read area from: ' + area_dir)
    
    # read time report
    time_dir = os.path.join(CWD, TOP_DIR, OUT_DIR, name + '_time.rpt')
    if os.path.exists(time_dir):
        with open(time_dir, 'r') as file:
            data = file.readlines()
            file.close()
        time = []
        for i,line in enumerate(data):
            if(line.startswith('Path 1:')):
                a = line.index('(')+1
                b = line.index(' ps)')
                time = int(line[a:b])
    if(time == -1):
        raise Exception('TCL_HELPER Error! Failed to read time from: ' + time_dir)

    # read power report
    power_dir = os.path.join(CWD, TOP_DIR, OUT_DIR, name + '_power.rpt')
    if os.path.exists(power_dir):
        with open(power_dir, 'r') as file:
            data = file.readlines()
            file.close()
        for i,line in enumerate(data):
            if(line.startswith('    Subtotal')):
                line_lst = line.split(' ')[::-1]
                for item in line_lst:
                    try:
                        temp_flt = float(item)
                        power = temp_flt
                        break
                    except:
                        continue
                break
    if(power == -1):
        raise Exception('TCL_HELPER Error! Failed to read power from: ' + power_dir)

    return area, CLOCK-time, power*1000

############################################## TEST ###############################################

if __name__ == '__main__':
    import random
    random.seed(43)
    name = 'test_1'
    l = [12 for i in range(39)]
    print(name,': Creating files...')
    create_files(name, MAIN_SCR)
    build_rtl(name, [VAR_D[i] for i in l], ADDER_MAP, MAIN_RTL) 
    p = run_tcl(name, True, MAIN_SCR)
    p.communicate()
    
    score = get_scores(name)
    print(name,':',score)

    print(name,': Done')