#include "evaluator16.h"

void read_vars(int var_num, uint8_t* vars){
    char buf;                                                           // input buffer
    int chk;                                                            // reach check value

    for(int i=0; i<var_num; i++){                                       // for every variable
        chk = fread(&buf, sizeof(uint8_t), 1, stdin);                   // read it
        if(chk==0){                                                     // if there is an error
            if(feof(stdin)){                                            // report it
                fwrite("[EOF error]", sizeof(char), 12, stderr);
                return;                                 
            }
            if(ferror(stdin)){
                fwrite("[stdin ERROR]", sizeof(char), 14, stderr);
                return;                                                 // and exit
            }
        }
        vars[i] = (uint8_t)buf;                                         // place it in the array
    }
    return;                                                             // return when done
}

string getExecutablePath() {
    // Get the path to this executable
    char buffer[4096];
    ssize_t len = readlink("/proc/self/exe", buffer, sizeof(buffer) - 1);
    if (len != -1) {
        buffer[len] = '\0';
    }
    return string(buffer);
}

uint64_t evaluate_MAE_16x16(uint8_t* vars){
    string exe_path = getExecutablePath();                              // this is needed because somehow c++ thinks that when opening a file
    filesystem::path exe_dir = filesystem::path(exe_path).parent_path();// with ifstream, the file is realative to the CWD of whoever called
    filesystem::path file_path = exe_dir / "inp.bin";                   // the executable instead of relative to the executable's directory
    ifstream inp_file(file_path, ios::binary );                         // file that contains test values
    if(!inp_file) {                                                     // !!! seriously, why does ifstream not throw an error
        fwrite("[file error] Failed to open inp.bin",                   // when you open a file that does not exist?
            sizeof(char), 36, stderr);                                  // It just returns random data if try to read it
        return 0xFFFFFFFFFFFFFFFF;                                      // like why? This should have been a segfault at the very least
    }

    uint32_t res, exp;                                                  // result value, expected value
    int32_t delta;                                                      // delta of expected - result
    uint16_t a,b;                                                       // input test values  
    uint64_t mae = 0;                                                   // mean average error
    
    for(int i=0; i<TEST_INP_16; i++){                                   // for every pair of test values
        inp_file.read(reinterpret_cast<char *>(&a), 2);                 // read them from the file
        inp_file.read(reinterpret_cast<char *>(&b), 2);                 // !!! Beware that the endianess is depended on your system architecture !!!
        exp = (uint32_t)a*(uint32_t)b;                                  // multiply (16-bit numbers still need to be casted to 32)
        res = ARCWM_16x16(a, b, vars);                                  // get the result of the approximate multiplier
        delta = res - exp;                                              // get the error
        mae = mae + (abs(delta)/TEST_INP_16);                           // add it's absolute value to the mean
    }

    inp_file.close();                                                   // close the test value file
    return mae;                                                         // return the resulting MAE
}

int main(){  
    uint8_t* vars = (uint8_t*) malloc(VAR_NUM_16*sizeof(uint8_t));          // allocate an array for variables
    for(int i=0; i<VAR_NUM_16; i++) vars[i] = 0;
    read_vars(VAR_NUM_16, vars);                                            // read variables from stdin into array
    uint64_t mae = evaluate_MAE_16x16(vars);                                // calculate MAE
    fwrite(&mae, sizeof(uint64_t),   1, stdout);                            // return MAE into stdout

    fflush(stdout);                                                         // flush output
    free(vars);                                                             // free array for variables
    return 0;                                                               // exit
}