param T = 10 integer;
param Nodes = 5; #no of nodes
param Nmax = 2; #no of agvs
param edgeCap = 1; #agvs on each edge
#param ep = 200; # edge penalty
#param nEdges = 2;


#---------------------------------#
set NODES = {0..Nodes-1} ;		 # set of nodes
set src;
set snk;
set nsrc = NODES diff src; 		 # to eliminate the sorce nodes from the set of nodes
set INT_NODES = nsrc diff snk;	 # to eliminate the sink the from the set obtained in the above step 

#set INT_NODES = nsrc inter nsnk;
#--------------------------------#

set TIME = {0..T};

#travelling times
param TAU {NODES,NODES};
var X {NODES,NODES,TIME}; # fromNode,toNode,time
var Y {NODES,TIME}; # nodeNo,time

maximize obj: sum{k in TIME,S in snk} (Y[S,k]);

s.t.
sink {l in TIME, S in snk}:
sum{i in NODES :l-TAU[i,S] >=0 } (X[i,S,l-TAU[i,S]]) = Y[S,l]; #constraint to neglect nodes that 
																		#	are not connected


inter {l in TIME, v0 in INT_NODES}:
sum{i in NODES :l-TAU[i,v0] >=0 } (X[i,v0,l-TAU[i,v0]]) = sum{j in NODES} X[v0,j,l];


source {l in TIME, D in src}:
sum{i in NODES} (X[D,i,l]) = Y[D,l];


#travelling capacity limit
travel {l in TIME, i in NODES,j in NODES}:
(sum{k in l..l+TAU[i,j]: k <= T } X[i,j,k]) <= edgeCap ;
cap {i in NODES, j in NODES, k in TIME}: 0 <= X[i,j,k] <= edgeCap;
noCircularFlow {i in NODES, k in TIME}: X[i,i,k] = 0;


#complete travel before T
travelComplete {i in NODES, j in NODES, k in T-TAU[i,j]+1..T: T-TAU[i,j]+1 >= 0 }: X[i,j,k] = 0;

endFlow: sum{k in TIME,S in snk,D in src} (Y[D,k] - Y[S,k]) = 0;

# restrict current number of AGVs for all k
netFlow {l in TIME, S in snk, D in src}: sum{k in 0..l} (Y[D,k] - Y[S,k]) <= Nmax
