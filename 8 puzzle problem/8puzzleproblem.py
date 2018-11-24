
import pydot

from time import time
graph=pydot.Dot(graph_type='digraph')


class Puzzle:
    # goal_state=[2,8,3,
    #             0,1,6,
    #             7,5,4]

    goal_state=[2,8,0,
                1,6,3,
                7,5,4]

    num_of_instances=0
    def __init__(self,state,parent,action,height):
        self.parent=parent
        self.state=state
        self.action=action
        self.height=height
        if self.is_goal():
            color="green"
        elif self.height>=5:
            color="red"
        else:
            color="yellow"
        self.graph_node = pydot.Node(str(self), style="filled", fillcolor=color)
        Puzzle.num_of_instances+=1

    def display(self):
        list=self.state
        string1=""
        for i in range(9):
            if (i + 1) % 3 != 0:
                if list[i]==0:
                    string1 += ("|   ")
                else:
                    string1+=("| %d "% list[i])
            else:
                if list[i]==0:
                    string1 += ("|   \n")
                else:
                    string1+=("| %d |\n" %list[i])
        string1+="\n"
        return string1

    def __str__(self):
        return self.display()

    def is_goal(self):
        if self.state == self.goal_state:
            return True
        return False

    @staticmethod
    def find_valid_actions(i,j):
        valid_action = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        if i == 0:  # up is disable
            valid_action.remove('UP')
        elif i == 2:  # down is disable
            valid_action.remove('DOWN')
        if j == 0:
            valid_action.remove('LEFT')
        elif j == 2:
            valid_action.remove('RIGHT')
        return valid_action

    def successors(self):
        children=[]
        x = self.state.index(0)
        i = int(x / 3)
        j = int(x % 3)
        valid_actions=self.find_valid_actions(i,j)
        height=self.height+1

        for action in valid_actions:
            new_state = self.state[:]
            if action is 'UP':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
                #children.append(Puzzle(new_state,self,action,height))
            elif action is 'DOWN':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
                #children.append(Puzzle(new_state,self,action,height))
            elif action is 'LEFT':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
                #children.append(Puzzle(new_state,self,action,height))
            elif action is 'RIGHT':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state,self,action,height))

        return children

    def get_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution


def breadth_first_search(initial_state):
    graph = pydot.Dot(graph_type='digraph', label="8 Puzzle State Space Using BFS algorithm", fontsize="30", color="red",
                      fontcolor="blue", style="filled", fillcolor="black")
    start_node = Puzzle(initial_state, None, None,0)
    if start_node.is_goal():
        return start_node.get_solution()
    frontier=[]
    frontier.append(start_node)
    explored=[]
    #print("The starting node is \nheight=%d\n" % start_node.height)
    print(start_node.display())
    while frontier:
        node=frontier.pop(0)
        #print("the node selected to expand is\n")
        #print("height=%d\n" % node.height)
        print(node.display())
        explored.append(node.state)
        graph.add_node(node.graph_node)
        #if node.parent:
            #graph.add_edge(pydot.Edge(node.parent.graph_node, node.graph_node,label=str(node.action)))
        if node.height<5:
            children=node.successors()
            #print("the children nodes of this node are\n")
            for child in children:
                if child.state not in explored :
                    #print("height=%d\n"%child.height)
                    #print(child.display())

                    if child.is_goal():
                        print("Goal state is obtained")
                        graph.add_node(child.graph_node)
                        graph.add_edge(pydot.Edge(child.parent.graph_node, child.graph_node, label=str(child.action)))
                        draw_legend(graph)
                        graph.write_png('statespace.png')
                        return child.get_solution()
                        break
                    graph.add_node(child.graph_node)
                    graph.add_edge(pydot.Edge(child.parent.graph_node, child.graph_node, label=str(child.action)))
                    frontier.append(child)
        else:
            print("exceeded limit\n")
    return

def draw_legend(graph):
    graphlegend = pydot.Cluster(graph_name="legend", label="Legend", fontsize="20", color="green",
                                fontcolor="blue", style="filled", fillcolor="white")

    legend1 = pydot.Node('Visited node', shape="plaintext")
    graphlegend.add_node(legend1)
    legend2 = pydot.Node("Reached max height", shape="plaintext")
    graphlegend.add_node(legend2)
    legend3 = pydot.Node('Goal Node', shape="plaintext")
    graphlegend.add_node(legend3)


    node1 = pydot.Node("1", style="filled", fillcolor="yellow", label="")
    graphlegend.add_node(node1)
    node2 = pydot.Node("2", style="filled", fillcolor="red", label="")
    graphlegend.add_node(node2)
    node3 = pydot.Node("3", style="filled", fillcolor="green", label="")
    graphlegend.add_node(node3)


    graph.add_subgraph(graphlegend)
    graph.add_edge(pydot.Edge(legend1, legend2, style="invis"))
    graph.add_edge(pydot.Edge(legend2, legend3, style="invis"))

    graph.add_edge(pydot.Edge(node1, node2, style="invis"))
    graph.add_edge(pydot.Edge(node2, node3, style="invis"))



def main():
    initial_state= [2, 8, 3,
                    1, 6, 4,
                    7, 0, 5]

    Puzzle.num_of_instances=0
    t0=time()
    solution=breadth_first_search(initial_state)
    t1=time()-t0
    print ("Solution:", solution)
    print ("space:", Puzzle.num_of_instances)
    print ("time:",t1,"seconds")


main()
