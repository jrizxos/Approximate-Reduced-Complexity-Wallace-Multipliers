import os
import time
import random
import traceback
from math import inf
from math import sqrt
from typing import List
from copy import deepcopy
from itertools import combinations
from subprocess import Popen, PIPE
from individual import individual, get_binary
from tcl_helper import create_files, build_rtl, run_tcl, get_scores
from score_tree import evaluated_individual, place_individual, store_tree, load_tree, find_individual, store_raw, load_raw
from config import VAR_N, VAR_D, BIT_W, MAIN_SCR, MAIN_RTL, MAIN_EVAL, ADDER_MAP, TCL_DEBUG, PROC_TIM, MAX_PROC, BST_N, POP_N, CLD_N, EVL_DEBUG, objectives, GEN_N, MUT_P

# Globals:
score_proc = []
combines_num = mutates_num = 0

def run_evaluation(vars:List[int], name:str):
    """Runs C++ evaluator and Genus synthesis for an Indiviual.
        Creates two processes and passes their variables via pipe.

        Args:
            None

        Returns:
            proc (Popen): created process
    """

    # run the synthesis
    create_files(name, MAIN_SCR)
    build_rtl(name, [VAR_D[i] for i in vars], ADDER_MAP, MAIN_RTL)
    proc_syn = run_tcl(name, TCL_DEBUG, MAIN_SCR)
    
    # run the MAE calculation
    if(not os.path.isfile(os.path.join('cppsim', MAIN_EVAL))):
        print('Warning: Evaluator not found, running make...')
        proc_make = Popen(os.path.join('.', 'cppsim', 'make'))
        proc_make.wait()
    command = os.path.join('.', 'cppsim', MAIN_EVAL)
    proc_cpp = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=False, text=False)
    inp = bytes(vars)
    inp_wrt = proc_cpp.stdin.write(inp)   # pass the input
    proc_cpp.stdin.flush()      # need to flush or else processes will deadlock
    if(EVL_DEBUG):
        print('running', name, ' ( pids -> cpp:', proc_cpp.pid, ', syn:', proc_syn.pid, ')')
        print('python wrote:', inp_wrt, 'bytes to', proc_cpp.pid)
    return proc_cpp, proc_syn

def wait_runs(comp, ln, TREE_ROOT):
    """Waits for all processes in score_proc to finish.
       Communicates and gets their output

        Args:
            None

        Returns:
            None
    """
    global score_proc

    if(len(score_proc) > 0):
        print('Run progress:', str(comp) + '/' + str(ln), 'runs...')
    while(len(score_proc) > 0):                                     # wait for all subprocesses to finish
        proc = score_proc.pop()

        if(EVL_DEBUG):
            print('waiting for process:', proc[0].pid, ', for individual:', proc[2].loaded_id)
        res, err = proc[0].communicate(timeout=PROC_TIM)            # update their values
        if(err!=b''):
            raise Exception("Evaluator did not read input vairables correctly! (" + str(err) + ")")
        try:
            proc[2].mae = int.from_bytes(res[:8], byteorder='little')
        except:
            raise Exception("Evaluator did not return valid data! (" + str(res) + ")")
        if(EVL_DEBUG):
            print('Done, got: ', res)
            print('waiting for process:', proc[1].pid, ', for individual:', proc[2].loaded_id)
        proc[1].wait(timeout=PROC_TIM)
        area, time, power = get_scores(proc[2].loaded_id)
        proc[2].area = area
        proc[2].time = time
        proc[2].power = power
        if(EVL_DEBUG):
            print('Done, got: ', proc[2].area, proc[2].time, proc[2].power)

        place_individual(proc[2], TREE_ROOT)
    return

def run_population(population:List[individual], force:bool, TREE_ROOT):
    """Runs the simulation for all individuals in input population one by one.

        Args:
            population (list of individuals): the individuals to run
            force (bool): if an individual has already been evaluated, force run again
        Returns:
            None
    """

    waits_num = 0
    for indiv in population:
        if(force or not evaluated_individual(indiv, TREE_ROOT)):              # check if already ran
            proc_cpp, proc_syn = run_evaluation(indiv.vars, indiv.loaded_id)  # run it
            score_proc.append((proc_cpp, proc_syn, indiv))                    # add to process list
            wait_runs(waits_num, len(population), TREE_ROOT)
        else:                                                                 # make sure that the values are loaded if already evaluated
            get_ind = find_individual(indiv, TREE_ROOT)
            indiv.loaded_id = get_ind.loaded_id
            indiv.mae = get_ind.mae
            indiv.area = get_ind.area
            indiv.time = get_ind.time
            indiv.power = get_ind.power
        waits_num += 1
    store_tree(TREE_ROOT)
    return

def run_population_parallel(population:List[individual], force:bool, TREE_ROOT):
    """Runs the simulation for all individuals in input population in parallel.

        Args:
            population (list of individuals): the individuals to run
            force (bool): if an individual has already been evaluated, force run again
        Returns:
            None
    """

    completed = 0
    while(completed < len(population)):                                             # run individuals  !! SLOW !!
        i = 0
        running = 0
        while(running < MAX_PROC):                                                  # slices list in groups of MAX_PROC individuals
            j = i+completed                                                         # index of current individual in population
            if(j >= len(population)):                                               # if out of bounds we are done
                break
            if(force or not evaluated_individual(population[j], TREE_ROOT)):        # skip any duplicates
                proc_cpp, proc_syn = run_evaluation(population[j].vars, population[j].loaded_id)
                score_proc.append((proc_cpp, proc_syn, population[j]))               # add to process list
                running += 1
            else:                                                                   # make sure that the values are loaded if already evaluated
                get_ind = find_individual(population[j], TREE_ROOT)
                population[j].loaded_id = get_ind.loaded_id
                population[j].mae = get_ind.mae
                population[j].area = get_ind.area
                population[j].time = get_ind.time
                population[j].power = get_ind.power
            i += 1
        wait_runs(completed, len(population), TREE_ROOT)                            # wait for all subprocesses in group to finish
        completed += MAX_PROC                                                       # proceed with next group, if it is last group then completed >=len(population)
    store_tree(TREE_ROOT)
    print()
    return

def tournament_selector(population:List[individual]):
    """Selects the best individuals from the population, based on tournament selection.

        Args:
            population (list of individuals): the population

        Returns:
            top (list of individual): selected individuals
    """
    top = []
    SAMPLES = 2                                         
    for _ in range(BST_N):
        pop_sample = random.sample(population, SAMPLES)
        partial_order_sort(pop_sample)
        top.append(pop_sample[0])

    if(EVL_DEBUG):
        print('selected:')
        print_population(top)
        
    return top

def get_ints(s:str):
    """Returns a list of ints from a binary string. This method also checks that the numbers returned
        are within the acceptable domain.

        Args:
            s (str): a binary string of length BIT_W*k

        Returns:
            vars (list of ints): the ints that correspond to every BIT_W bits of input
    """
    vars = []
    for i in range(BIT_W, len(s)+1, BIT_W):         # for every BIT_W bits
        val = int(s[i-BIT_W:i],base=2)              # find the int that corresponds to them in list
        if(val >= len(VAR_D)):                      # if the int is not within the domain
            val = random.choice(range(len(VAR_D)))  # pick a random value for it
        vars.append(val)                            # put it in the list
    return vars

def binary_combinator(A:individual, B:individual):
    """Combines individuals A and B, based on binary combination method with a single random crossover point.

        Args:
            A (individual): first individual
            B (individual): second individual

        Returns:
            [C1,C2] (list of individuals): two new children
    """
    global combines_num
    A_bits = B_bits = ''
    for var_A,var_B in zip(A.vars, B.vars):
        A_bits += get_binary(var_A)
        B_bits += get_binary(var_B)

    point = random.choice(range(len(A_bits)))
    mask = [True for i in range(point)] + [False for i in range(len(A_bits) - point)]

    child_bits_1 = ''
    child_bits_2 = ''
    for i,choice in enumerate(mask):
        if choice:
            child_bits_1 += A_bits[i]
            child_bits_2 += B_bits[i]
        else:
            child_bits_1 += B_bits[i]
            child_bits_2 += A_bits[i]
    
    C1 = individual(get_ints(child_bits_1), 'cm-'+str(combines_num))
    combines_num+=1
    C2 = individual(get_ints(child_bits_2), 'cm-'+str(combines_num))
    combines_num+=1
    return [C1,C2]

def mate(top:List[individual]):
    """Combines top individuals to produce a specified number of children.

        Args:
            top (list of individuals): individuals to be mate (expected sorted)

        Returns:
            children (list of individuals): new children generated
    """
    global TREE_ROOT
    children = []
    comb = list(combinations([x for x in range(len(top))], 2))      # these are the total possible ways to combine the individuals of input
    skipped = []                                                    # list of skipped combinations
    for i in range(len(comb)):                                      # limit those to the total number of childern we asked for
        idx_A = comb[i][0]                                          # creating two children per loop
        idx_B = comb[i][1]
        if(top[idx_A].loaded_id == top[idx_B].loaded_id):           # if they are the same individuals skip this combination
            skipped.append(comb[i])
            continue
        C = binary_combinator(top[idx_A],top[idx_B])                # combine the children
        children.append(C[0])                                       # and add them to the list
        children.append(C[1])
        if(len(children)>=CLD_N):
            break
    i = 0
    while(len(children)<CLD_N):                                     # still need more children ?                        
        idx_A = skipped[i][0]                                       # creating using the skipped combinations now
        children.append(deepcopy(top[idx_A]))                       # since in this combination the parents are the same
        children.append(deepcopy(top[idx_A]))                       # both children will be the same as the parent
        i += 1

    children = children[:CLD_N]                                     # if the number of children is odd, ditch the last child

    run_population_parallel(children, False, TREE_ROOT)             # find their scores
    if(EVL_DEBUG):
        print('new children:')
        print_population(children)

    return children                                        

def binary_mutation(A:individual):
    """Mutates individual A using binary mutation. Inveses one bit of A.

        Args:
            A (individual): individual to be mutated

        Returns:
            new_indiv (individual): mutated individual
    """
    global mutates_num
    A_bits = ''
    for var_A in A.vars:
        A_bits += get_binary(var_A)
    
    curr_idx = random.randrange(0,len(A_bits))                                              # select index of bit to mutate
    new_bit = '1' if A_bits[curr_idx]=='0' else '0'                                         # inverse that bit
    A_bits = A_bits[:curr_idx] + new_bit + A_bits[curr_idx+1:]
    new_indiv = individual(get_ints(A_bits), 'mt-'+str(mutates_num))
    mutates_num+=1
    return new_indiv

def mutate(population:List[individual]):
    """Mutates the population in-place.

        Args:
            population (list of individuals): individuals to be mutated

        Returns:
            None
    """
    global TREE_ROOT

    mutated = []
    old = []
    for i,indiv in enumerate(population):                               # iterate children for mutation
        if(random.random()<MUT_P):
            new_indiv = binary_mutation(indiv)                          # mutate individuals
            if(EVL_DEBUG):
                print('mutated:', indiv.loaded_id, '->', new_indiv.loaded_id)
            mutated.append(new_indiv)                                   # create new mutated individual
            old.append(i)
    run_population_parallel(mutated, False, TREE_ROOT)                  # find the new individuals' scores

    for i,new_indiv in zip(old,mutated):                                # swap new individuals with old ones
        population.pop(i)                                               # remove old one
        population.append(new_indiv)                                    # add new
    return

def create_init(size:int = POP_N):
    """Creates an initial population of individuals.

        Args:
            size (int): create a population with specific size

        Returns:
            population (list of individuals): generated initial population
    """
    global EVL_DEBUG, TREE_ROOT

    if(size>POP_N):
        size = POP_N

    population = []
    for i in range(size):
        population.append(individual(None, 'in-'+str(i)))   

    run_population_parallel(population, False, TREE_ROOT)

    return population

def dominates(A:individual, B:individual):
    """Returns A dominates B (A < B). This means that A is better or equal to B in all aspects.
        As defined by NSGA-II algorithm. If A == B returns false (A does not dominate itself).

        Args:
            A (individual): dominant (?) individual
            B (individual): dominated(?) individual

        Returns:
            (A < B) (Bool): true if A<B, else false
    """
    if(A.mae == B.mae and           # it's unlikely that two different individuals will have
       A.area == B.area and         # exactly the same evalutation values, but in that case
       A.time == B.time and         # still no-one dominates
       A.power == B.power):
        return False
    
    if(A.mae <= B.mae and           # A dominates B
       A.area <= B.area and
       A.time <= B.time and
       A.power <= B.power):
        return True
    
    return False                    # A does not dominate B

def partial_order(A:individual, B:individual):
    """Returns partial order of A and B (A <n B). This means that A is partially preceding B.
        As defined by NSGA-II algorithm.

        Args:
            A (individual): preceding (?) individual
            B (individual): succeding (?) individual

        Returns:
            (A <n B) (Bool): true if A <n B, else false
    """
    if(A.rank < B.rank or 
       (A.rank == B.rank and A.distance > B.distance)):
        return True
    return False

def fast_non_dominated_sort(population:List[individual]):
    """Returns the non dominated fronts of a population of individuals,
        while assigning a rank to each individual.
        As defined by NSGA-II algorithm.

        Args:
            population (list of individuals): the total population

        Returns:
            fronts (list of list of individuals): the non-dominated fronts
    """
    fronts = [[]]
    for p in population:
        p.dominates = []
        p.dom_count = 0
        for q in population:
            if(dominates(p,q)):
                p.dominates.append(q)
            elif(dominates(q,p)):
                p.dom_count += 1
        if(p.dom_count == 0):
            p.rank = 0
            fronts[0].append(p)

    i = 0
    while(len(fronts[i])!=0):
        Q = []
        for p in fronts[i]:
            for q in p.dominates:
                q.dom_count -= 1
                if(q.dom_count == 0):
                    q.rank = i+1
                    Q.append(q)
        i += 1
        fronts.append(Q)

    if(EVL_DEBUG):  
        for i,f in enumerate(fronts):
            print('front',str(i)+':')
            if(len(f)==0):
                print('<empty front>\n')
            else:
                print_population(f) 

    return fronts

def crowding_distance_assignment(population:List[individual]):
    """Assigns a crowding distance to each individual in the input population.
        Intended to be used for non-dominated fronts. The distance is dependent
        on all the front individuals, not the individuals of the total population.
        As defined by NSGA-II algorithm.

        Args:
            population (list of individuals): individuals of a non-dominated front 
    
        Returns:
            None
    """
    global objectives

    if(len(population)==0):
        return
    for i in population:
        i.distance = 0
    for objective in objectives:
        population.sort(key = lambda x : getattr(x,objective))
        population[0].distance = population[-1].distance = inf
        for i in range(1,len(population)-1):
            dist = (getattr(population[i+1],objective) - getattr(population[i-1],objective))/objectives[objective]
            population[i].distance += dist
    return

def partial_order_sort(population:List[individual]):
    """Sorts a population of individuals in-place. Using partial order of individuals (A <n B).
        This means that A is partially preceding B, by either having a smaller rank, or in case
        of equal ranks a bigger crowding distance.
        As defined by NSGA-II algorithm.

        Args:
            population (list of individuals): list of individuals to sort in-place

        Returns:
            None
    """
    population.sort(key = lambda x: x.rank)
    population.sort(key = lambda x: x.distance, reverse=True)
    return

def print_population(population:List[individual]):
    ''' Prints a population in a squared fashion.

        Args:
            population (list of individuals): population to print

        Returns:
            None
    '''

    L = len(population)
    cols = int(sqrt(L))
    max_str = max(population, key = lambda x:len(x.loaded_id))
    spacer = len(max_str.loaded_id) + 1
    print('length =',L)
    for i in range(0,L,cols):
        for j in range(0,cols):
            if(i+j>=L):
                break
            c = population[i+j].loaded_id
            len_c = spacer - len(c)
            print(' '*len_c+c, end='')
        print()
    print()
    return

def search(restore_pareto=None):
    """Searches the search space using NSGA-II.

        Args:
            restore_pareto (str): name of the json file containing a pareto front to use as initial population

        Returns:
            population (list of individual): pareto front of nondominated solutions
    """
    global TREE_ROOT, EVL_DEBUG, MUT_P, GEN_N, POP_N

    ######################### INTIAL POPULATION #########################
    print('Creating initial population...')
    if(restore_pareto!=None):                                                  # restore from pareto
        population = load_raw(FILE=restore_pareto)
        if(len(population)<POP_N):                                              # if it has less individuals than needed
            population += create_init(POP_N-len(population))                    # add more
        elif(len(population)>POP_N):                                            # if it has more
            population = population[:POP_N]                                     # remove from the end
    else:
        population = create_init()                                              # create a brand new random population
    print('initial population:')
    print_population(population) 

    P_fronts = fast_non_dominated_sort(population)
    for front in P_fronts:
        crowding_distance_assignment(front)

    ############################### SEARCH ##############################
    print('\nSearching...')
    generation = 1                                                              # number of generations processed
    try:
        while(generation<=GEN_N):
            print('\nGeneration:', str(generation) + '/' + str(GEN_N))

            # New population (pre-NSGA-II)
            top = tournament_selector(population)                               # select top individuals
            children = mate(top)                                                # make new chidren
            mutate(children)                                                    # mutate the chidren
            population += children                                              # add children to population            
            
            print('Q population:')
            print_population(population) 

            # NSGA-II
            R_fronts = fast_non_dominated_sort(population)
            selected = []
            i = 0
            while(len(selected) + len(R_fronts[i]) < POP_N):
                crowding_distance_assignment(R_fronts[i])
                selected += R_fronts[i]
                i+=1
            crowding_distance_assignment(R_fronts[i])                           # this was a slight oversight in the original algorithm
            partial_order_sort(R_fronts[i])
            selected += R_fronts[i][:POP_N-len(selected)]
            population = selected                                               # keep best

            print('P population:')
            print_population(population)
                
            # Evolution control
            generation += 1                                                     # increment generation counter
            store_raw(population)

    except Exception as e:
        print(traceback.format_exc())
        print('Search failed:', str(e))
        for p in score_proc:
            p[0].kill()
            p[1].kill()
        
    return population

def run_static(IUT:List[individual], TREE_ROOT):
    """Runs specific individuals in IUT. This will evaluate the individuals in IUT and update the
        <highscore_entries> and highscores.json with their results. Nothing is returned.

        Args:
            IUT (list of individuals): individuals under testing

        Returns:
            None
    """
    global score_proc

    try:
        run_population_parallel(IUT, False, TREE_ROOT)
    except Exception as e:
        print(traceback.format_exc())
        print('Static run failed:', str(e))
        for p in score_proc:
            p[0].kill()
            p[1].kill()
    return

def run_spread_samples(N:int):
    global TREE_ROOT

    IUT = []
    for i in range(N):
        IUT.append(individual(None, str(i)))

    run_static(IUT)

    store_tree(TREE_ROOT)
    return

############################################## Main ###############################################
if __name__ == '__main__':

    t = time.time()

    TREE_ROOT = load_tree()
    search()
    
    t = time.time() - t
    print('Search done!')
    if(t>3600):
        print('(in',t/3600,'hours)')
    elif(t>60):
        print('(in',t/60,'minutes)')   
    else:
        print('(in',t,'seconds)')
