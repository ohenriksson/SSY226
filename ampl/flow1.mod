
# k in {0..T}
#  y0 --x1--> y1 --x2--> y2

param T = 10 integer;
param Tau1 = 2;
param Tau2 = 3;


param E = 2; #no of edges
param Nmax = 1; #no of agvs
param edgeCap = 1;

var x1 {0..T} integer; #edge 1
var x2 {0..T} integer; #edge 2

var y0 {0..T} integer; #source
var y2 {0..T} integer; #sink


maximize obj: sum{k in 0..T} (y2[k]);

s.t.
s1 {k in Tau2..T}: x2[k-Tau2] = y2[k]; #sink vertex
s2 {k in Tau1..T}: x1[k-Tau1] = x2[k]; #transfer vertex
s3 {k in 0..T}: x1[k] = y0[k]; # source vertex

#travelling capacity limit
travel1 {k in 0..T-Tau1}: (sum{t in k..k+Tau1-1} x1[t]) <= edgeCap ;
travel2 {k in 0..T-Tau2}: (sum{t in k..k+Tau2-1} x2[t]) <= edgeCap ;

#--might not be needed because of the above constraint
cap1 {k in 0..T}: 0 <= x1[k] <= edgeCap;
cap2 {k in 0..T}: 0 <= x2[k] <= edgeCap;

#complete travel before T
travelcomplete1 {k in T-Tau1+1..T}: x1[k] = 0;
travelcomplete2 {k in T-Tau2+1..T}: x2[k] = 0;

#what flows out from the source has to flow into the sink
endFlow: sum{k in 0..T} (y0[k]-y2[k]) = 0;

#max number of AGVS in the network:
flow {t in 0..T} : sum{k in 0..t} (y0[k]-y2[k]) <= Nmax;
#flow {k in 0..T-Tau2}: sum{t in k..k+Tau2} (x1[t] + x2[t]) <= Nmax+1 #alternative approach

