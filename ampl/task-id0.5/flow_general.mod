param T = 10 integer;
param nrTask = 2 integer;
param nrNodes = 5 integer;
param Nodes = 3; #no of nodes
param Nmax = 2; #no of agvs
param edgeCap = 1; #agvs on each edge
#param ep = 200; # edge penalty

#param nEdges = 2;

set NODES = {0..nrNodes-1};
#set INT_NODES = {src+1..snk-1};
set TIME = {0..T};
set task = {1..nrTask};

param src {t in task};
param snk {t in task};
param int {task, NODES};

#travelling times
param TAU {NODES,NODES};
var X {NODES,NODES,TIME}; # fromNode,toNode,time
var Y {NODES,TIME}; # nodeNo,time

maximize obj: sum{k in TIME, t in task} (Y[snk[t],k]);

s.t.
sink {l in TIME, t in task}:
sum{i in NODES :l-TAU[i,snk[t]] >=0 } (X[i,snk[t],l-TAU[i,snk[t]]]) = Y[snk[t],l];
inter {l in TIME, t in task}:
sum{i in NODES :l-TAU[i,int[t,i]] >=0 } (X[i,int[t,i],l-TAU[i,int[t,i]]]) = sum{j in NODES: l-TAU[j,int[t,j]] >= 0 } X[int[t,j],j,l];
source {l in TIME, t in task}:
sum{i in NODES} (X[src[t],i,l]) = Y[src[t],l];


#travelling capacity limit
travel {l in TIME, i in NODES,j in NODES}:
(sum{k in l..l+TAU[i,j]: k <= T } X[i,j,k]) <= edgeCap ;
cap {i in NODES, j in NODES, k in TIME}: 0 <= X[i,j,k] <= edgeCap;
noCircularFlow {i in NODES, k in TIME}: X[i,i,k] = 0;


#complete travel before T
travelComplete {i in NODES, j in NODES, k in T-TAU[i,j]+1..T: T-TAU[i,j]+1 >= 0 }: X[i,j,k] = 0;

endFlow: sum{k in TIME, t in task} (Y[src[t],k] - Y[snk[t],k]) = 0;

# restrict current number of AGVs for all k
netFlow {l in TIME}: sum{k in 0..l, t in task} (Y[src[t],k] - Y[snk[t],k]) <= Nmax