#!/usr/bin/python


import commands
import random
import sys
import networkx as nx


max_color = 3
arestes_c = []
alo_cnf = []
amo_cnf = []
num_vars = 0
num_clauses = 0
solution = []
edge_probability = 0.0
llista_nodes = []
colors = {
'1' : "#00FFFF",
'2' : "#00CC99",
'3' : "#00FF00",
'4' : "#FFFF00",
'5' : "#FF0000",
'6' : "#FFA31A",
'7' : "#8000FF",
'8' : "#CC00CC",
'9' : "#FFB3D9",
'10' : "#800000",
'11' : "#336600",
'12' : "#000099",
'13' : "#CCCCFF",
'14' : "#660066",
'15' : "#000000",
}
G = nx.Graph()
#create cnf for edge
def code_aresta(node1,node2):
    global num_vars
    global num_clauses
    global arestes_c
    global max_color

    for i in range(1, int(max_color)+1):
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
    print "llista_nodes: ", llista_nodes

#write cnf in file
def write_cnf():
    global num_vars
    global num_clauses
    global arestes_c
    global alo_cnf
    global amo_cnf

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

    for item in amo_cnf:
        if item == 0:
            file.write("0")
            file.write("\n")
        else:
            file.write(str(item))
            file.write(" ")


    file.close()

#create clausules amo
def create_alo():
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

def create_amo():
    global num_vars
    global amo_cnf
    global max_color
    global num_nodes
    global num_clauses

    for y in range(1, int(num_nodes)+1):
        for i in range(1, int(max_color)+1):
            for x in range(i+1, int(max_color)+1):

                amo_cnf.append(-i)
                amo_cnf.append(-x)
                amo_cnf.append(0)
                num_clauses = num_clauses +1


def create_graph():

    global max_color
    global num_nodes
    global edge_Probability
    global G

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
    global llista_nodes

    A = nx.nx_agraph.to_agraph(G)
    A.node_attr['style'] = 'filled'
    A.node_attr['width'] = '0.4'
    A.node_attr['height'] = '0.4'
    A.edge_attr['color'] = '#000000'
    for i in range(1, num_nodes+1):
        color  = colors.get(str(int(llista_nodes[i-1])%(int(max_color))+1))
        print color
        A.get_node(i).attr['fillcolor'] = color

    print "print solution",solution

    A.layout()
    A.draw("out.png", format='png')

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
        num_nodes = int(sys.argv[1])
        max_color = int(sys.argv[2])
        edge_Probability = float(sys.argv[3])
    else:
        print "Format Error: Arguments invalids cargats els per defecte\nFormat: graph.py <nodes> <number colors> <edge probability>"

def main():
    global solution
    global max_color
    global llista_nodes
    global G

    read_parameters()
    create_graph()
    create_alo()
    create_amo()
    write_cnf()
    parse_solution()
    assignar_colorete(solution)
    draw_graf()


if __name__ == '__main__':
    main()
