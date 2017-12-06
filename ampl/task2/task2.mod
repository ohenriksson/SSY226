
param nrAGVs; # Number of AGVs.
param T; # Time limit.
set TIME = {0..T};

# --- LAYOUT PROPERTIES
param edgeCap; # Limitation of AGVs running beside each other.
param startNode; # Where the AGVs inital starts.
param endNode;   # opposite to above
param travelTask; # Task ID for travelling purpose between nodes.
param taskLowerBound = 1;


set NODES = {0..endNode};

set ARCS within {NODES,NODES}; # Pair of connecting nodes.
set INTER = NODES diff {startNode,endNode}; # Set of intermediate nodes (in- and out-flow).
param TAU {ARCS}; # Time cost for each arc.
param epsilon;

#---TASK PROPERTIES
param nTasks; # Number of tasks.
set TASK = {0..nTasks};
set TASKLIST = TASK diff {travelTask};

param src_tasks {TASKLIST}; #source for each task
param snk_tasks {TASKLIST}; #sink for each task

#---VARIABLES
var X {NODES,NODES,TASK,TIME} integer >= 0, <= edgeCap; # Indicator for sending an AGV on an arc.
var Y {NODES,TASK,TIME} integer >= 0; # Indicator for an AGV arriving at a node


#---OBJ FUNCTION
maximize obj: sum{k in TIME, tsk in TASKLIST} Y[snk_tasks[tsk], tsk ,k];

#---CONSTRAINTS
s.t.
detector {k in TIME, t in TASK, v0 in NODES}: sum{(i,v0) in ARCS: k-TAU[i,v0] >=0} X[i,v0,t,k-TAU[i,v0]] = Y[v0,t,k];
#preventEarlyStart {k in TIME, (i,j) in ARCS, t in TASK :k-TAU[i,j] < 0}: Y[j,t,k] = 0;


#--inflow = outflow
flowCtrl {k in TIME, v0 in INTER}:
sum {t in TASK, (i,v0) in ARCS: k-TAU[i,v0] >=0} X[i,v0,t,k-TAU[i,v0]] =
sum {(v0,j) in ARCS, t in TASK} X[v0,j,t,k];


#--continue with an ongoing task
tasksMustGoOn {k in TIME, t in TASKLIST, n in INTER:
n != src_tasks[t] and n != snk_tasks[t] }:  Y[n,t,k] = sum {(n,j) in ARCS} X[n,j,t,k];


#--if a task reaches it's destination it has to release
taskMustBeDropped {k in TIME, t in TASKLIST, n in INTER: n == snk_tasks[t]}:
sum {(n,j) in ARCS} X[n,j,t,k] = 0;

travelling {k in TIME, t in TASKLIST, n in INTER: n == snk_tasks[t]}:
sum {(n,j) in ARCS, t2 in TASKLIST: n != src_tasks[t2]} X[n,j,t2,k] = 0;

# --agvs in the intermediate nodes at t=0
# nAGVs_interStart: sum{t in TASK, i in INTER} Y[i,t,0] = 0;
restrictAGVs: sum {k in TIME, (startNode,j) in ARCS, t in TASK} X[startNode,j,t,k] <= nrAGVs;


#--arctravel num of AGVs travelling on an arc.
#travel {k in TIME, (i,j) in ARCS}:
#sum {k_win in k..k+TAU[i,j]-1, t in TASK: k_win <= T} (X[i,j,t,k_win]) <= edgeCap;

#travel constraint using epsilon
travel {k in TIME, (i,j) in ARCS}:
sum {k_win in k..k+epsilon-1, t in TASK: k_win <= T} (X[i,j,t,k_win]) <= edgeCap;




restrictStartNodeTask: # (always use task 0 since it is not in tasklist)
sum {k in TIME, t in TASKLIST, (startNode,j) in ARCS} X[startNode,j,t,k] = 0;


# Restrict how many times a task is allowed to be done
restrictTask {t in TASKLIST}: taskLowerBound <= sum {k in TIME} (Y[snk_tasks[t],t,k])
