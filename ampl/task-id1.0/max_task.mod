param T; # Time limit.
param nrTask; # Number of task.
param nrNodes; # Number of nodes.
param nrAGVs; # Number of AGVs. 
param edgeCap; # Limitation of AGVs running beside each other.

set NODES = {0..nrNodes-1}; 
set TIME = {0..T}; 
set TASK = {1..nrTask};

set ARCS within {NODES,NODES}; # Pair of connecting nodes.

set SRC; # Set of nodes, start of a task (out-flow).
set SNK; # Set of nodes, end of a task (in-flow).
set INTER; # Set of intermediate nodes (in- and out-flow).

set LINK within {SRC,SNK}; # Pair of sorces and sinks.

param TAU {ARCS}; # Time cost for each arc.
param TASK_ID {LINK}; # Task ID for each pair of sources and sinks.
param AT {TASK,NODES};

var X {NODES,NODES,TASK,TIME} integer >= 0, <= edgeCap; # Indicator for sending an AGV on an arc.
var Y {NODES,TASK,TIME} integer >= 0; # Indicator for an AGV at a node.

maximize obj: sum{k in TIME, (sr,sn) in LINK} (Y[sn,TASK_ID[sr,sn],k]);

s.t.
# Constraint for AGVs arriving to a sink node.
sink {k in TIME, (sr,sn) in LINK, t in TASK}:
sum {(i,sn) in ARCS: k-TAU[i,sn] >= 0} (X[i,sn,t,k-TAU[i,sn]]) = Y[sn,t,k];
# Constraint for balancing at a node.
inter {k in TIME, v0 in INTER, t in TASK}:
sum {(i,v0) in ARCS: k-TAU[i,v0] >=0} (X[i,v0,t,k-TAU[i,v0]]) = sum{(v0,j) in ARCS} (X[v0,j,t,k]);
# Constraint for AGVs leaving a source node.
source {k in TIME, (sr,sn) in LINK, t in TASK}:
sum {(sr,j) in ARCS} (X[sr,j,t,k]) = Y[sr,t,k];

# Constraint for the number of AGVs travelling on an arc.
travel {k in TIME, (i,j) in ARCS}:
sum {k_win in k..k+TAU[i,j]-1, t in TASK: k_win <= T} (X[i,j,t,k_win]) <= 1;

# Only allow the AGVs to do the task restricted to that source node
AllowedTask {k in TIME, src in SRC, t in TASK: AT[t,src] == 0}: Y[src,t,k] = 0;

# Restrict how many times a task is allowed to be done
restrictTask {(src,snk) in LINK}: 0 <= sum {k in TIME} (Y[snk,TASK_ID[src,snk],k]) <= 1;


# Constraint for always finish a started task.
endFlow {(sr,sn) in LINK}: sum {k in TIME} (Y[sr,TASK_ID[sr,sn],k] - Y[sn,TASK_ID[sr,sn],k]) = 0;

# Constraint for number of AGVs running in the system.
netFlow {k in TIME}: 
0 <= sum {k_cum in 0..k, (sr,sn) in LINK} (Y[sr,TASK_ID[sr,sn],k_cum] - Y[sn,TASK_ID[sr,sn],k_cum]) <= nrAGVs; 