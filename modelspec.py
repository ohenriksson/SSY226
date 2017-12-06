# modelspec.py:



# --- Layout Specifications

# pickup                            place
#   o
#   o                               [ ]
#   o   --delivery_distance-->      [ ]
#   o                               [ ]
#   o

pickup_stations = 2
place_stations =  2
delivery_distance = 2#[m] distance in x direction (euclidian distances will be computed)



# --- Optimization Specifications
n_agvs = 2
agv_velocity = 1 #[m/s]

# --- DANGER ZONE
allow_tel_back_to_pickup = False #should AGVs teleport back when a task is completed or
intermidiate_layers = 1 #layer inbetween pickup and place nodes
unique_tasks = max(pickup_stations,place_stations)+3 #number of unique deliveries
intermidiate_nodes = max(pickup_stations,place_stations) #num of nodes for each intermidiate layer
node_spacing_y = 2 #height space between each node
edge_capacity = 1 #number of AGVs on the same arc
timeframe = 40 #[s] The timeframe within tasks will be maximized
epsilon = 1 #number of time units one agv occupies an arc
all_tasks = 1 #number of times all tasks at least should be done
