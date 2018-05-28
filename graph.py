#!/usr/bin/python

import networkx as nx
#import pygraphviz
import commands
import sys
import random

max_color = 3
arestes_c = []
alo_cnf = []
num_vars = 0
num_clauses = 0
solution = []
edge_Probability = 0.0
llista_nodes = []
colors = {
'1' : "00FFFF",
'2' : "00CC99",
'3' : "00FF00",
'4' : "FFFF00",
'5' : "FF0000",
'6' : "FFA31A",
'7' : "8000FF",
'8' : "CC00CC",
'9' : "FFB3D9",
'10' : "800000",
'11' : "336600",
'12' : "000099",
'13' : "CCCCFF",
'14' : "660066",
'15' : "000000",
}

#create cnf for edge
def code_aresta(node1,node2):
    global num_vars
    global num_clauses
    global arestes_c
    global max_color

    for i in range(1, max_color+1):
        arestes_c.append(-((node1-1)*max_color+i))
        arestes_c.append(-((node2-1)*max_color+i))
        arestes_c.append(0)
        num_clauses = num_clauses +1


#assign color to node        
def assignar_colorete(solution):
	global max_color
	global llista_nodes
	llista_nodes = []
	solutionfound = False
	cont = 0
	for item in solution:
		cont = cont + 1
		if item > 0 and solutionfound == False:
			llista_nodes.append(item)
			solutionfound = True
		if cont > int(max_color)-1:
			solutionfound = False
			cont = 0
	print "llista_nodes: ",llista_nodes

#write cnf in file
def write_cnf():
    global num_vars
    global num_clauses
    global arestes_c
    global alo_cnf

    file = open("testfile.txt","w") 
    file.write("c Random CNF formula\n") 
    file.write("p cnf ")
    file.write(str(num_vars))
    file.write(" ")
    file.write(str(num_clauses))
    file.write("\n")

    for item in alo_cnf:
        if item == 0:  
            file.write("0") 
            file.write("\n") 
        else:
            file.write(str(item))
            file.write(" ")
   
    for item in arestes_c:
        if item == 0:  
            file.write("0") 
            file.write("\n") 
        else:
            file.write(str(item))
            file.write(" ") 
 
    file.close()

#create clausules amo
def create_amo():
    global max_color
    global alo_cnf
    global num_vars
    global num_clauses

    alo_cnf = []
    num = 0

    for y in range(1, int(num_nodes)+1):
        for i in range(1, int(max_color)+1):
            num = num + 1
            alo_cnf.append(num)
            num_vars = num_vars +1
        alo_cnf.append(0)
        num_clauses = num_clauses +1

def create_graph():

    global max_color
    global num_nodes
    global edge_Probability
	global G

    G = nx.Graph()
    #G = nx.complete_graph(num_nodes)
  

    #create nodes
    for i in range(1,int(num_nodes)+1):
        G.add_node(i)

    #create edges
    for i in range(1,int(num_nodes)+1):
        for j in range(1,int(num_nodes)+1):
            if i < j and random.random() < edge_Probability:
                G.add_edge(i, j)
                print "a fet aresta de ",i," a ",j
                code_aresta(i,j)
    
    #A = to_agraph(G)
    #G.layout()
    #G.draw("G.png", format='png')

def draw_graf():
	global solution
	global colors
	global max_color
	global G

	for i in range(1, int(num_nodes)+1):
		G.get_node(i).attr['fillcolor'] = G.color_codes[colors.get((int(llista_nodes[i-1])%(int(max_color) ))+1)]
    
	print "print solution",solution
  
def parse_solution():
    global solution
    
    startload = False
    next_number_negative = False
    result = commands.getoutput('./spiderman.py testfile.txt')
    solution = []
    print result
    for item in result:
        if item == "v":
            startload = True
        elif startload == True:
            if item != " ":
                if item == "-":
                    next_number_negative = True
                else:
                    if next_number_negative == True:
                        solution.append(int(item)*-1)
                        next_number_negative = False
                    else:
                        solution.append(int(item))
    
    print "solution",solution    
    
def read_parameters():

    global solution
    global max_color
    global num_nodes
    global edge_Probability

    #default values
    max_color = 3
    num_nodes = 3
    edge_Probability = 0.5
      
    if len(sys.argv) == 4:        
        num_nodes = sys.argv[1]
        max_color = sys.argv[2]
        edge_Probability = sys.argv[3]
    else:   
        print "Format Error: Arguments invalids cargats els per defecte\nFormat: graph.py <nodes> <number colors> <edge probability>"
		
def main():
	global solution
	global max_color
	global llista_nodes
	global G

	read_parameters()
	create_graph() 
	create_amo()
	write_cnf()
	parse_solution()
	assignar_colorete(solution)
    draw_graf()

	G.a_graph.layout()
	G.a_graph.draw("out.png", format = 'png')

if __name__ == '__main__': 
    main()
    


