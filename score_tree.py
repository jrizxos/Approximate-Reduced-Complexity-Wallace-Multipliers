import os
import json
from individual import individual
from config import VAR_N

MAX_DEPTH = VAR_N

class Node:
    """ Simple node class """
    def __init__(self, num, leaf):
        self.var = num          # an integer
        self.children = []      # node's children nodes
        self.leaf = leaf        # None if node is not a leaf, the individual represented by the path if it is a leaf

    def find_child(self, num):
        """ Finds is a number is within the children of this node.

        Args:
            num (int): a number to find in children

        Returns:
            cild (Node | None): if the number is found within the childen, else returns None
        """
        found = None
        for child in self.children:
            if(child.var == num):
                found = child
                break
        return found
    
    def add_child(self, num, leaf):
        """ Adds a child to this node.

        Args:
            num (int): number of the child
            leaf (individual): the individual represented by the path if child is a leaf

        Returns:
            cild (Node): the child just added
        """
        self.children.append(Node(num,leaf))
        return self.children[-1]

def find_individual(A:individual, TREE_ROOT:Node):
    """ Finds an individual in a tree. Used to confirm whether or not the individual is in the tree.

        Args:
            A (individual): the individual to look up
            TREE_ROOT (Node): the root node of the tree to search

        Returns:
            The same individual A if found, None if the individual is not in the tree.
    """
    vars = A.vars
    depth = 0
    current = TREE_ROOT
    while(current.leaf==None):
        next = current.find_child(vars[depth])
        if(next==None):
            return None
        current = next
        depth += 1
    return current.leaf

def evaluated_individual(A:individual, TREE_ROOT:Node):
    """ Finds individual in a tree and returns whether or not the individual has been evaluated

        Args:
            A (individual): the individual to look up
            TREE_ROOT (Node): the root node of the tree to search

        Returns:
            False if at least one of the evaluation values is missing
            True if the individual has been evaluated
    """
    get_ind = find_individual(A, TREE_ROOT)
    if(get_ind==None):
        return False
    elif(get_ind.mae==None or 
         get_ind.area==None or 
         get_ind.time==None or 
         get_ind.power==None):
        return False
    return True

def place_individual(A:individual, TREE_ROOT:Node):
    """ Places an individual on the tree, if the individual is already on the tree it overwrites it.

        Args:
            A (individual): the individual to look up
            TREE_ROOT (Node): the root node of the tree to add to

        Returns:
            None
    """
    current = TREE_ROOT
    for depth, val in enumerate(A.vars):
        if(depth==MAX_DEPTH-1):
            next = current.find_child(val)
            if(next==None):
                current.add_child(val, A)
            else:
                next.leaf = A
        else:
            next = current.find_child(val)
            current = current.add_child(val, None) if next==None else next
    return

def load_tree(FILE = 'highscores.json'):
    """ Loads a tree from a json file onto a tree data structure.

        Args:
            File (str): json file name

        Returns:
            TREE_ROOT (Node): the root of the tree data structure
    """
    TREE_ROOT = Node(None, None)
    if(os.path.exists(os.path.join(os.getcwd(), FILE))):
        with open(FILE, 'r') as json_file:                              # load json db
            json_object = json.load(json_file)
            json_file.close()
            for entry in json_object:                                   # for every object in db
                raw_entry = json_object[entry]  
                indiv = individual(raw_entry['solution'], 'ld-'+str(entry))    # make a new individual with those values
                indiv.mae = raw_entry['mae']
                indiv.area = raw_entry['area']
                indiv.time = raw_entry['time']
                indiv.power = raw_entry['power']
                place_individual(indiv, TREE_ROOT)                      # place it in the tree
    return TREE_ROOT

def json_dumper(entr_dict, FILE):
    """ json.dumps, but better. It structures the output so it's human readable. 
        Why is this not in the library by default?

        Args:
            entr_dict (dict): data to dump to file
            File (str): json file name to dump to 

        Returns:
            TREE_ROOT (Node): the root of the tree data structure
    """
    json_object = '{\n'
    entries = list(entr_dict.keys())
    for entry in entries:
        json_object += '\"' + str(entry) + '\":{\n'
        keys = list(entr_dict[entry].keys())
        for key in keys:
            json_object += '\t\"' + str(key) + '\":'
            json_object += str(entr_dict[entry][key]) + (',\n' if key!=keys[-1] else '\n')
        json_object += '\t},\n' if entry!=entries[-1] else '\t}\n'
    json_object += '}'
    
    with open(FILE, 'w') as json_file:
        json_file.write(json_object)
        json_file.close()

def store_tree(TREE_ROOT, FILE = 'highscores.json'):
    """ Stores individuals from a tree data structure to a json file.

        Args:
            TREE_ROOT (Node): the root of the tree data structure
            File (str): json file name

        Returns:
            None
    """
    entr_dict = {}
    entries_num = 0
    #DFS
    stack = [(TREE_ROOT,[])]        # stack item: node and path to node
    while(len(stack)>0):
        v = stack.pop()
        node = v[0]
        path = v[1] + ([node.var] if node.var!=None else [])   # update current node's path
        if(node.leaf != None):
            ind = node.leaf
            entr_dict[entries_num] = {"solution" : path, "mae" : ind.mae, "area" : ind.area, "time" : ind.time, "power" : ind.power}
            entries_num += 1
        for child in node.children:
            stack.append((child, path))

    json_dumper(entr_dict, FILE)
    return

def load_raw(FILE = 'pareto.json'):
    """Loads a list of individuals from a json file.

        Args:
            File (str): json file name

        Returns:
            highscore_entries (list of individuals): loaded values and scores
    """
    highscore_entries = []
    nosol = False
    if(os.path.exists(os.path.join(os.getcwd(), FILE))):
        with open(FILE, 'r') as json_file:                              # load json db
            json_object = json.load(json_file)
            for id in json_object:                                      # for every object in db
                raw_entry = json_object[id]
                if('solution' in raw_entry):                          
                    indiv = individual(raw_entry['solution'], 'lr-'+id)     # make a new individual with those values
                else:
                    indiv = individual([], 'lr-'+id)                        # this is specifically for evoapprox multipliers
                    nosol = True
                indiv.mae = raw_entry['mae']
                indiv.area = raw_entry['area']
                indiv.time = raw_entry['time']
                indiv.power = raw_entry['power']
                highscore_entries.append(indiv)                 # add it to dict
        json_file.close()  
        if(nosol):
            print("Waring: multipliers with no solution in", FILE)
    else:
        print('Warning: file',os.path.join(os.getcwd(), FILE),'not found!')
    return highscore_entries

def store_raw(results, FILE = 'pareto.json'):
    """ Stores a list of individuals to a json file.

        Args:
            results (list of individuals): individuals to store
            File (str): json file name

        Returns:
            None
    """
    entr_dict = {}
    for i,ind in enumerate(results):
        entr_dict[i] = {"solution" : ind.vars, "mae" : ind.mae, "area" : ind.area, "time" : ind.time, "power" : ind.power}

    json_dumper(entr_dict, FILE)
    return

############################################## TEST ###############################################

if __name__ == '__main__':
    TREE_ROOT = load_tree('highscores.json')
    store_tree(TREE_ROOT, 'highscores2.json')
    highscore_entries = load_raw()

    for entry in highscore_entries:
        if(find_individual(entry, TREE_ROOT)==None):
            print('woah')
            break

    print('Done')