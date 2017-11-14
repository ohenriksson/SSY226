
var a;
var r;

param T_level = 10;

param T = 15;

param A_cost = 0;
param T_cost = 1;
param R_cost = 1;

minimize obj: a;

s.t.
time: T_cost*T_level + R_cost*r <= T;
flowIn: a + r - t == 0;
p1: a >= 1;
p3: r >= 0;


