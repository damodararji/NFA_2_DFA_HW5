import json
from collections import OrderedDict

with open('input.json') as file:
    data = json.load(file)

dfa_states = 2 ** data["states"]
dfa_letters = data["letters"]
dfa_start = data["start"]
x = []
y = []
z = []
o = []

o.append((dfa_start,))

nfa_transitions = {}
dfa_transitions = {}

for transition in data["t_func"]:
    nfa_transitions[(transition[0], transition[1])] = transition[2]

for input_State in o:
    for symbol in dfa_letters:
        if len(input_State) == 1 and (input_State[0], symbol) in nfa_transitions:
            dfa_transitions[(input_State, symbol)] = nfa_transitions[(input_State[0], symbol)]

            if tuple(dfa_transitions[(input_State, symbol)]) not in o:
                o.append(tuple(dfa_transitions[(input_State, symbol)]))
        else:
            dest = []
            f_dest =[]

            for nth_state in input_State:
                if (nth_state, symbol) in nfa_transitions and nfa_transitions[(nth_state, symbol)] not in dest:
                    dest.append(nfa_transitions[(nth_state, symbol)])
            
            if dest:
                for d in dest:
                    for value in d:
                        if value not in f_dest:
                            f_dest.append(value)
            
                dfa_transitions[(input_State, symbol)] = f_dest 

                if tuple(f_dest) not in o: 
                    o.append(tuple(f_dest))

for key, value in dfa_transitions.items():
    temp_list = [[key[0], key[1], value]]
    x.extend(temp_list)


for o_state in o:
    for g_state in data["final"]:
        if g_state in o_state:
            y.append(o_state)

dfa = OrderedDict()
dfa["states"] = dfa_states
dfa["letters"] = dfa_letters
dfa["t_func"] = x
dfa["start"] = dfa_start
dfa["final"] = y

output_file = open('output.json', 'w+')
json.dump(dfa, output_file, separators = (',\t' , ':'))