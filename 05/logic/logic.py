# -*- coding: utf-8 -*-
from helpimport import *
import Findresolvents

#The clauses should be given in a .cls (Text) file, each line a clause
#literals separated through blank spaces, negative literals with - infront of them.
#Example: 
#a -c -d
#c -a
#It have to be horn clauses (clauses with no more than one positive literal ). 

def main(knowledgebase, printfenster, goal):
    if knowledgebase:
        #enter goal, get queue "goal" with the goal as only item:
        if not goal.empty():   
            #list to remember which goals you already had in your goal queue:
            oldgoals=[]
            oldgoals.append(goal.queue[0])
            #do the resolution:
            answer=resolution(knowledgebase,goal,oldgoals,"y",printfenster)   
            printfenster.insert(END, "The goal has been "+answer+".\n" )
            
    return

def printresolvent(clause,ind1,clause2,printfenster):
## to print a clause during resolution in a way you can see from which clauses it results 
# Input:
#   -clause (new clause you want to print)
#   -ind1 (first parent clause index)
#   -clause2 (second parent clause)
# Output:
#   --------    
    if (clause or clause==[]):
        printfenster.insert(END,"R(C"+str(ind1)+","+str(clause2)+")\n =" +str(clause)+"\n" )
        
    else:
        printfenster.insert(END,"R(C"+str(ind1)+","+str(clause2)+")\n = nothing \n" )
        
    
def newgoals(goal,new,oldgoals,answer,check,parentAindex,parentB,printfenster):
    ## puts new goals in goal queue if they haven't been used before + prints resolvents if check==y
# Input: 
#   -goal (current queue of goals), will be changed in case of new goals
#   -new (clause-candidates for new goals)
#   -oldgoals (all goals that have been within the queue goal before -to avoid duplicates)
#   -answer ("not found" or "found")
#   -check ('y' if you want to print results of each resolutionstep, else 'n')
#   -parentAindex (index of parent clause in KB), only needed if check==y
#   -parentB (other parent clause (the current goal, not necessarily in KB)), only needed if check==y
#   -printfenster (to print on the GUI)
# Output:
#   -goal (updated queue of goals)
#   -answer ("not found" or "found"), becomes "found" if [] in new.
    if new:
        if [] in new:
            if check=="y":
                printresolvent([],parentAindex,parentB,printfenster)
            answer="found"
        else:
            #if there are new goals, add them to queue goal:
            n=0
            while n<len(new):
                if check=="y":
                    printresolvent(new[n],parentAindex,parentB,printfenster)
                if not new[n] in oldgoals:
                    goal.put(new[n])
                    oldgoals.append(new[n])
                    n=n+1
    else:
        if check=="y":
            printresolvent("",parentAindex,parentB,printfenster)
    return [goal,answer]
  
def resolution(KB,goal,oldgoals,check,printfenster):
## Resolution over the set of clauses "KB" and the queue "goal":
# Input:
#   -KB (list of clauses)
#   -goal (LIFO queue you want to resolve from), may be changed within the function
#   -oldgoals (all goals that have been within the queue goal before -to avoid duplicates), may be changed within the function
#   -check ('y' if you want to print results of each resolutionstep, else 'n')
#   -printfenster (to print on the GUI)
# Output: 
#   -answer ("not found" or "found")
    answer="not found"
    if not len(KB)==0 and not goal.empty():
        firstgoal=goal.get()
        for r in KB:     
            #find all resolvents of the first goal and the clause with r in KB:
            new=Findresolvents.resolvents(r,firstgoal)
            # put new goals in goal queue if they haven't been used before + prints resolvents if check==y
            update=newgoals(goal,new,oldgoals,answer,check,KB.index(r),firstgoal,printfenster)
            goal=update[0]
            answer=update[1]
            if answer=="found":
                return answer
            #do the resolution again with the updated goal queue:
            answer=resolution(KB,goal,oldgoals,check,printfenster)
            if answer=="found":
                return answer
    return answer
