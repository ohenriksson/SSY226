# modelspec.py:



# --- Layout Specifications

# pickup                            place
#   o
#   o                               [ ]
#   o   --delivery_distance-->      [ ]
#   o                               [ ]
#   o

pickup_stations = 3 
place_stations = 4
delivery_distance = 4 #[m] distance in x direction (euclidian distances will be computed)
grid_layout = True #arcs are only connected to neighbouring nodes

# --- Optimization Specifications
n_agvs = 2
agv_velocity = 1 #[m/s]


# --- DANGER ZONE
allow_tel_back_to_pickup = True#should AGVs teleport back when a task is completed or
intermidiate_layers = 1 #layer inbetween pickup and place nodes
unique_tasks = max(pickup_stations,place_stations) #number of unique deliveries
intermidiate_nodes = max(pickup_stations,place_stations) #num of nodes for each intermidiate layer
node_spacing_y = 2 #height space between each node
edge_capacity = 1 #(epsilon is used atm, this has no effect) number of AGVs on the same arc
epsilon = 1 #number of time units one agv occupies an arc
all_tasks = 1 #number of times all tasks at least should be done
