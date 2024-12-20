#include "evaluator8.h"

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

uint32_t evaluate_MAE_8x8(uint8_t* vars){
    uint32_t res, exp;                                                  // result value, expected value and MAE
    int32_t delta;                                                      // delta of expected - result
    uint8_t a,b;                                                        // input test values  
    uint32_t mae = 0;

    for(int i=0; i<TEST_INP_8; i++){
        for(int j=0; j<TEST_INP_8; j++){
            exp = (uint32_t)i*(uint32_t)j;                              // multiply 
            res = (uint32_t)ARCWM_8x8((uint8_t)i, (uint8_t)j, vars);    // get the result of the approximate multiplier
            delta = res - exp;                                          // get the error
            mae = mae + abs(delta);                                     // add it's absolute value to the mean
        }
    }
    return mae/(TEST_INP_8*TEST_INP_8);                                 // return the resulting MAE
}

/////////////////////////////////////////// main //////////////////////////////////////////
int main(){  
    uint8_t* vars = (uint8_t*) malloc(VAR_NUM_8*sizeof(uint8_t));           // allocate an array for variables
    for(int i=0; i<VAR_NUM_8; i++) vars[i] = 0;
    read_vars(VAR_NUM_8, vars);                                             // read variables from stdin into array
    uint32_t mae = evaluate_MAE_8x8(vars);                                  // calculate MAE
    fwrite(&mae, sizeof(uint32_t),   1, stdout);                            // return MAE into stdout

    fflush(stdout);                                                         // flush output
    free(vars);                                                             // free array for variables
    return 0;                                                               // exit
}