
param nrAGVs; # Number of AGVs.
param T; # Time limit.
set TIME = {0..T};

# --- LAYOUT PROPERTIES
param nrNodes; # Number of nodes.
param edgeCap; # Limitation of AGVs running beside each other.
param startNode; # Where the AGVs inital starts.
param travelTask; # Task ID for travelling purpose between nodes.
param endNode;

set NODES = {0..nrNodes-1};

#set LINK within {SRC,SNK}; # Pair of sorces and sinks.
set ARCS within {NODES,NODES}; # Pair of connecting nodes.
set INTER = NODES diff {startNode,endNode}; # Set of intermediate nodes (in- and out-flow).

param TAU {ARCS}; # Time cost for each arc.

#---TASK PROPERTIES
param nTasks; # Number of tasks.
set TASK = {1..nTasks};
set TASKLIST = {1..nTasks};

param src_tasks {TASKLIST}; #source for each task
param snk_tasks {TASKLIST}; #sink for each task

#param TASK_ID {LINK}; # Task ID for each pair of sources and sinks.
param AT {TASK,NODES}; # Allowed task on this node

#---VARIABLES
var X {NODES,NODES,TASK,TIME} integer >= 0, <= edgeCap; # Indicator for sending an AGV on an arc.
var Y {NODES,TASK,TIME} integer >= 0; # Indicator for an AGV arriving at a node


#---OBJ FUNCTION
maximize obj: sum{k in TIME, tsk in TASKLIST} (Y[snk_tasks[tsk], tsk ,k]);

#---CONSTRAINTS
s.t.
detector {k in TIME, t in TASK, v0 in NODES}: sum{(i,v0) in ARCS: k-TAU[i,v0] >=0} X[i,v0,t,k-TAU[i,v0]] = Y[v0,t,k];

#preventEarlyStart {k in TIME, (i,j) in ARCS, t in TASK :k-TAU[i,j] < 0}: Y[j,t,k] = 0;
#preventLateEnd {k in TIME, (i,j) in ARCS, t in TASK :k+TAU[i,j] >= T}: X[i,j,t,k] = 0;


#--inflow = outflow
flowCtrl {k in TIME, v0 in INTER}:
sum {t in TASK, (i,v0) in ARCS: k-TAU[i,v0] >=0} X[i,v0,t,k-TAU[i,v0]] =
sum {(v0,j) in ARCS, t in TASK} X[v0,j,t,k];

/*
#--continue with an ongoing task
tasksMustGoOn {k in TIME, t in TASKLIST, n in INTER, (i,n) in ARCS:
  k-TAU[i,n] >=0 and n != snk_tasks[t] and n != src_tasks[t]}:
(X[i,n,t,k-TAU[i,n]]) = sum{(n,j) in ARCS} (X[n,j,t,k]);
*/


# --agvs in the intermediate nodes at t=0
nAGVs_interStart: sum{t in TASK, i in INTER} Y[i,t,0] = 0;
restrictAGVs: sum {k in TIME, (src,snk) in ARCS, t in TASK:src==startNode} X[src,snk,t,k] <= nrAGVs;


#--arctravel num of AGVs travelling on an arc.
travel {k in TIME, (i,j) in ARCS}:
sum {k_win in k..k+TAU[i,j]-1, t in TASK: k_win <= T} (X[i,j,t,k_win]) <= edgeCap;




/*
flowStartEnd:
sum {k in TIME, t in TASK, (i,endNode) in ARCS: k-TAU[i,endNode] >=0} (X[i,endNode,t,k-TAU[i,endNode]]) =
sum {k in TIME, (startNode,j) in ARCS, t in TASK} (X[startNode,j,t,k]);

/*

#

# Only allow the AGVs to do the task restricted to that source node
#AllowedTask {k in TIME, i in NODES, t in TASK: i != startNode and AT[t,i] == 0}: Y[i,t,k] = 0;

# Restrict how many times a task is allowed to be done
#restrictTask {(src,snk) in LINK}: 0 <= sum {k in TIME} (Y[snk,TASK_ID[src,snk],k]) <= 1;

# Constraint for always finish a started task.
#taskFlow {(sr,sn) in LINK}: sum {k in TIME} (Y[sr,TASK_ID[sr,sn],k] - Y[sn,TASK_ID[sr,sn],k]) = 0;

# endFlow: sum{k in TIME, t in TASK, (startNode,j) in ARCS} (X[startNode,j,t,k]) = sum{k in TIME, t in TASK, (i,endNode) in ARCS} (X[i,endNode,t,k]);
*/
