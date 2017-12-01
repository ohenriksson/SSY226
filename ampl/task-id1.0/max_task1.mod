param T; # Time limit.
param nrTask; # Number of task.
param nrNodes; # Number of nodes.
param nrAGVs; # Number of AGVs. 
param edgeCap; # Limitation of AGVs running beside each other.
param startNode; # Where the AGVs inital starts.
param travelTask; # Task ID for travelling purpose between nodes. 
param endNode;

set NODES = {0..nrNodes+1}; 
set TIME = {0..T}; 
set TASK = {travelTask..nrTask};

set ARCS within {NODES,NODES}; # Pair of connecting nodes.

param SOURCE_TASK{TASK};
param SINK_TASK{TASK};
set SRC; # Set of nodes, start of a task (out-flow).
set SNK; # Set of nodes, end of a task (in-flow).
set INTER; # Set of intermediate nodes (in- and out-flow).

set LINK within {SRC,SNK}; # Pair of sorces and sinks.

param TAU {ARCS}; # Time cost for each arc.
param TASK_ID {LINK}; # Task ID for each pair of sources and sinks.
param AT {TASK,NODES};

var X {NODES,NODES,TASK,TIME} integer >= 0, <= edgeCap; # Indicator for sending an AGV on an arc.
var Y {NODES,TASK,TIME} integer >= 0; # Indicator for an AGV at a node.

maximize obj: sum{k in TIME, (src,snk) in LINK} (Y[snk,TASK_ID[src,snk],k]);

s.t.

detect {k in TIME, (i,j) in ARCS, t in TASK: k-TAU[i,j] >= 0}: X[i,j,t,k-TAU[i,j]] = Y[j,t,k];
preventEarlyStart {k in TIME, (i,j) in ARCS, t in TASK :k-TAU[i,j] < 0}: Y[j,t,k] = 0;
preventLateEnd {k in TIME, (i,j) in ARCS, t in TASK :k+TAU[i,j] >= T}: X[i,j,t,k] = 0;



#inflow = outflow
flowCtrl {k in TIME, v0 in INTER}:
sum {t in TASK, (i,v0) in ARCS: k-TAU[i,v0] >=0} (X[i,v0,t,k-TAU[i,v0]]) = sum{(v0,j) in ARCS, t in TASK} (X[v0,j,t,k]);


flowStartEnd:
sum {k in TIME, t in TASK, (i,endNode) in ARCS: k-TAU[i,endNode] >=0} (X[i,endNode,t,k-TAU[i,endNode]]) =
sum {k in TIME, (startNode,j) in ARCS, t in TASK} (X[startNode,j,t,k]);


#continue with an ongoing task
#tasksMustGoOn {k in TIME, t in TASK, n in INTER, (i,n) in ARCS: t != travelTask and k-TAU[i,n] >=0 and n != SINK_TASK[t] and n != SOURCE_TASK[t]}:
#(X[i,n,t,k-TAU[i,n]]) = sum{(n,j) in ARCS} (X[n,j,t,k]);

# Restrict number of AGVs in the system.
#restrictAGVs: sum {k in TIME, (startNode,src) in ARCS, (src,snk) in LINK} (X[startNode,src,TASK_ID[src,snk],k]) <= nrAGVs;

# Constraint for the number of AGVs travelling on an arc.
#travel {k in TIME, (i,j) in ARCS}:
#sum {k_win in k..k+TAU[i,j]-1, t in TASK: k_win <= T} (X[i,j,t,k_win]) <= 1;

test {k in TIME, i in NODES, t in TASK}: Y[i,t,k] <= 1;


# Only allow the AGVs to do the task restricted to that source node
#AllowedTask {k in TIME, i in NODES, t in TASK: i != startNode and AT[t,i] == 0}: Y[i,t,k] = 0;

# Restrict how many times a task is allowed to be done
#restrictTask {(src,snk) in LINK}: 0 <= sum {k in TIME} (Y[snk,TASK_ID[src,snk],k]) <= 1;

# Constraint for always finish a started task.
#taskFlow {(sr,sn) in LINK}: sum {k in TIME} (Y[sr,TASK_ID[sr,sn],k] - Y[sn,TASK_ID[sr,sn],k]) = 0;

# endFlow: sum{k in TIME, t in TASK, (startNode,j) in ARCS} (X[startNode,j,t,k]) = sum{k in TIME, t in TASK, (i,endNode) in ARCS} (X[i,endNode,t,k]);
