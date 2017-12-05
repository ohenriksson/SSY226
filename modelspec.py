# modelspec.py:



# --- Layout Specifications

# pickup                            place
#   o
#   o                               [ ]
#   o   --delivery_distance-->      [ ]
#   o                               [ ]
#   o

pickup_stations = 4
place_stations =  5
delivery_distance = 40  #[m] distance in x direction (euclidian distances will be computed)



# --- Optimization Specifications
timeframe = 10 #[s] The timeframe within tasks will be maximized
n_agvs = 2
agv_velocity = 1 #[m/s]


allow_tel_back_to_pickup = False #should AGVs teleport back when a task is completed or
intermidiate_layers = 1


