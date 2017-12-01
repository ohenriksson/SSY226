
param nrAGVs; # Number of AGVs.
param T; # Time limit.
set TIME = {0..T};

# --- LAYOUT PROPERTIES
param nrNodes; # Number of nodes.
param edgeCap; # Limitation of AGVs running beside each other.
param startNode; # Where the AGVs inital starts.
param endNode;   # opposite to above
param travelTask; # Task ID for travelling purpose between nodes.

set NODES = {0..nrNodes-1};

set ARCS within {NODES,NODES}; # Pair of connecting nodes.
set INTER = NODES diff {startNode,endNode}; # Set of intermediate nodes (in- and out-flow).
param TAU {ARCS}; # Time cost for each arc.

#---TASK PROPERTIES
param nTasks; # Number of tasks.
set TASK = {0..nTasks};
set TASKLIST = TASK diff {0};

param src_tasks {TASKLIST}; #source for each task
param snk_tasks {TASKLIST}; #sink for each task

#---VARIABLES
var X {NODES,NODES,TASK,TIME} integer >= 0, <= edgeCap; # Indicator for sending an AGV on an arc.
var Y {NODES,TASK,TIME} integer >= 0; # Indicator for an AGV arriving at a node


#---OBJ FUNCTION
maximize obj: sum{k in TIME, tsk in TASKLIST} (Y[snk_tasks[tsk], tsk ,k]);

#---CONSTRAINTS
s.t.
detector {k in TIME, t in TASK, v0 in NODES}: sum{(i,v0) in ARCS: k-TAU[i,v0] >=0} X[i,v0,t,k-TAU[i,v0]] = Y[v0,t,k];
#preventEarlyStart {k in TIME, (i,j) in ARCS, t in TASK :k-TAU[i,j] < 0}: Y[j,t,k] = 0;


#--inflow = outflow
flowCtrl {k in TIME, v0 in INTER}:
sum {t in TASK, (i,v0) in ARCS: k-TAU[i,v0] >=0} X[i,v0,t,k-TAU[i,v0]] =
sum {(v0,j) in ARCS, t in TASK} X[v0,j,t,k];


#--continue with an ongoing task
tasksMustGoOn {k in TIME, t in TASKLIST, n in NODES:
n != src_tasks[t] and n != snk_tasks[t] }:  Y[n,t,k] = sum {(n,j) in ARCS} X[n,j,t,k];

#--if a task reaches it's destination it has to release
taskMustBeDropped {k in TIME, t in TASKLIST, n in NODES: n == snk_tasks[t]}:
sum {(n,j) in ARCS} X[n,j,t,k] = 0;



/*
#-- net task flow cannot increase for a task that does not has it's source here
taskChangeCheck {k in TIME, t in TASKLIST, n in NODES: n!=src_tasks[t]}: Y[n,t,k]
*/

# --agvs in the intermediate nodes at t=0
nAGVs_interStart: sum{t in TASK, i in INTER} Y[i,t,0] = 0;
restrictAGVs: sum {k in TIME, (src,snk) in ARCS, t in TASK:src==startNode} X[src,snk,t,k] <= nrAGVs;

#--arctravel num of AGVs travelling on an arc.
travel {k in TIME, (i,j) in ARCS}:
sum {k_win in k..k+TAU[i,j]-1, t in TASK: k_win <= T} (X[i,j,t,k_win]) <= edgeCap;

flowStartEnd:
sum {k in TIME, t in TASK, (i,endNode) in ARCS } Y[endNode,t,k] =
sum {k in TIME, (startNode,j) in ARCS, t in TASK} (X[startNode,j,t,k]);

restrictStartNodeTask: # (always use 0 since it is not in tasklist)
sum {k in TIME, t in TASKLIST, (startNode,j) in ARCS} X[startNode,j,t,k] = 0;

# Restrict how many times a task is allowed to be done
#restrictTask {(src,snk) in LINK}: 0 <= sum {k in TIME} (Y[snk,TASK_ID[src,snk],k]) <= 1;
