param T = 12 integer;
param Nodes = 3; #no of nodes
param Nmax = 2; #no of agvs
param edgeCap = 1; #agvs on each edge
param ep = 200; # edge penalty

param src = 0;
param snk = Nodes-1;
param nEdges = 2;

set NODES = {src..snk};
set INT_NODES = {src+1..snk-1};
set TIME = {0..T};

set LINKS within {NODES,NODES};
param TAU {LINKS};

#travelling times
var X {NODES,NODES,TIME}; # fromNode,toNode,time
var Y {NODES,TIME}; # nodeNo,time

maximize obj: sum{k in TIME} (Y[snk,k]);

s.t.
sink {l in TIME}:
sum{(i,snk) in LINKS: l-TAU[i,snk] >= 0 } (X[i,snk,l-TAU[i,snk]]) = Y[snk,l];
inter {l in TIME, v0 in INT_NODES}:
sum{(i,v0) in LINKS: l-TAU[i,v0] >= 0 } (X[i,v0,l-TAU[i,v0]]) = sum{(v0,j) in LINKS} X[v0,j,l];
source {l in TIME}:
sum{(src,j) in LINKS} (X[src,j,l]) = Y[src,l];

#travelling capacity limit
travel {l in TIME, (i,j) in LINKS}:
(sum{k in l..l+TAU[i,j]-1: k <= T } X[i,j,k]) <= edgeCap ;
cap {(i,j) in LINKS, k in TIME}: 0 <= X[i,j,k] <= edgeCap;
noCircularFlow {i in NODES, k in TIME}: X[i,i,k] = 0;

#complete travel before T
#travelComplete {(i,j) in LINKS, k in T-TAU[i,j]+1..T: T-TAU[i,j]+1 >= 0 }: X[i,j,k] = 0;

endFlow: sum{k in TIME} (Y[src,k] - Y[snk,k]) = 0;

# restrict current number of AGVs for all k
netFlow {l in TIME}: sum{k in 0..l} (Y[src,k] - Y[snk,k]) <= Nmax
