param T = 50 integer;
param nrTask = 2 integer;
param Nodes = 5; #no of nodes
param Nmax = 2; #no of agvs
param edgeCap = 1; #agvs on each edge
#param ep = 200; # edge penalty

#param nEdges = 2;

set NODES = {0..Nodes-1};
#set INT_NODES = {src+1..snk-1};
set TIME = {0..T};
set task = {1..nrTask};

param src {t in task};
param snk {t in task};
param tau {t in task};

set ARCS within {NODES,NODES};
set INTER within {task, NODES};

#travelling times
param TAU {ARCS};
param interNodes{INTER};

var X {NODES,NODES,TIME} integer; # fromNode,toNode,time
var Y {NODES,TIME}; # nodeNo,time

maximize obj: sum{k in TIME, t in task} (Y[snk[t],k]);

s.t.
sink {l in TIME, t in task}:
sum{(i,snk[t]) in ARCS: l-TAU[i,snk[t]] >= 0 } (X[i,snk[t],l-TAU[i,snk[t]]]) = Y[snk[t],l];
inter {l in TIME, t in task, (t,j) in INTER}:
sum{(i,j) in ARCS: l-TAU[i,j] >= 0} (X[i,j,l-TAU[i,j]]) = sum{(j,i) in ARCS} X[j,i,l];
source {l in TIME, t in task}:
sum{(src[t],j) in ARCS} (X[src[t],j,l]) = Y[src[t],l];


#travelling capacity limit
travel {l in TIME, (i,j) in ARCS}:
(sum{k in l..l+TAU[i,j]-1: k <= T } X[i,j,k]) <= edgeCap;
cap {(i,j) in ARCS, k in TIME}: 0 <= X[i,j,k] <= edgeCap;
noCircularFlow {i in NODES, k in TIME}: X[i,i,k] = 0;



#complete travel before T
#travelComplete {i in NODES, j in NODES, k in T-TAU[i,j]+1..T: T-TAU[i,j]+1 >= 0 }: X[i,j,k] = 0;

#endFlow: sum{k in TIME, t in task} (Y[src[t],k] - Y[snk[t],k]) = 0;
endFlow {t in task}:
sum{k in TIME} (Y[src[t],k] - Y[snk[t],k]) = 0;

#endFlow2 {t in task, l in TIME: l+tau[t] <= T}: Y[src[t],l] = Y[snk[t],l+tau[t]];


# restrict current number of AGVs for all k
netFlow {l in TIME}: sum{k in 0..l, t in task} (Y[src[t],k] - Y[snk[t],k]) <= Nmax;