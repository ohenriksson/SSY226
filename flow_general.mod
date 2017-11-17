


param T = 10 integer;

param Nodes = 3; #no of nodes
param Nmax = 1; #no of agvs
param edgeCap = 1; #agvs on each edge



param src = 0;
param snk = Nodes-1;
param nEdges = 2;


set NODES = {src..snk};

set TAU = {2..3,2..3};

var X {NODES,NODES,0..T}; # fromNode,toNode,time
var Y {NODES,0..T}; # nodeNo,time



maximize obj: sum{k in 0..T} (Y[snk,k]);

s.t.
sink {tau in TAU, k in tau..T}: Y[snk,k] = (sum{i in NODES} X[i,snk,k-TAU[i,snk]] );
inter {k in TAU[0]..T, i in src+1..snk-1}: 
(sum{j in NODES} X[j,i,k-TAU[j]] ) =  ( sum{j in src..snk} X[i,j,k] );

source {k in 0..T}: Y[src,k] = (sum{i in src..snk} X[src,i,k] );


#travelling capacity limit
travel {k in 0..T-Tau[0], i in src..snk, j in src..snk}: 
(sum{l in k..k+Tau[i]} X[i,j,l]) <= edgeCap ;

cap {k in 0..T, i in src..snk, j in src..snk}: 0 <= X[i,j,k] <= edgeCap;

noCircularFlow {i in src..snk, k in 0..T}: X[i,i,k] = 0;


#complete travel before T
travelComplete1 {i in src..snk, j in src..snk, k in T-Tau[i]+1..T}: X[i,j,k] = 0;
travelComplete2 {i in src..snk, j in src..snk, k in T-Tau[j]+1..T}: X[j,i,k] = 0;

endFlow: sum{k in 0..T} (Y[snk,k] - Y[src,k]) = 0;



# restrict current number of AGVs for all k
netFlow {k in 0..T}: sum{l in 0..k} (Y[snk,l] - Y[src,l]) <= Nmax

