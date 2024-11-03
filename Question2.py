#Imported all the modules that will be used
import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn; seaborn.set_style("whitegrid")
from scipy.signal import find_peaks 

#Function used to calculate mass
def calcMass(density):
  return density * vol

#Function calculates Drag force in x direction based on particle motion
def dragForceX(vx):
  if vx <= 0:
    return  -0.5 * drag_coefficient * fluid_density * vx**2 * area
  else:
    return 0.5 * drag_coefficient * fluid_density * vx **2 * area

#Function calculates Drag force in x direction based on particle motion

def dragForceY(vy):
  if vy <= 0:
    return  -0.5 * drag_coefficient * fluid_density * vy**2 * area
  else:
    return 0.5 * drag_coefficient * fluid_density * vy **2 * area

# Time Data
t_initial = 0
t_final = 2                       
dt = 0.001
t_value = np.arange(t_initial,t_final,dt)

# Sphere properties
diameter = 0.0286                              # diameter, [m]
area = (math.pi * diameter**2)/4             # area, [m^2]
vol = 4/3 * math.pi * (diameter/2)**3        # volume, [m^3] of foam ball
density = 23                   # [kg/m^3] of the foam ball
mass = calcMass(density)          # [kg]

#Gravity
g = -9.81  

# Initial position
rx = 0                        # [m]
ry = 1                        # [m]
if rx < 0 or ry > 0:          # if rx or ry changed to any position below ground this is the default values set up
    ry = 1                     
    rx = 0 
# Initial velocity
vx = 0                        # [m/s]
vy = 0                        # [m/s]

# Fluid properties
fluid_density = 1.25                   # [kg/m^3]
drag_coefficient = 0.05

# Coefficient of restitution
coeff_restitution = 0.47                


    # Initial components of velocity- as the ball is dropping, the starting position has no values
vx = 0        # [m/s]
vy = 0        # [m/s]

    # The for loop iterates through all values in step intervals of initial to final time    
for i in range(len(t_value)):
  plt.plot(i, ry,color='black', marker='o', linestyle='dashed',linewidth=2, markersize=2)
  plt.xlabel("Horizontal Displacement ")
  plt.ylabel("Vertical Displacement")
  plt.title("Empirical Model ")

  plt.grid()

        # Gravity
  weight = calcMass(density) * g
        
        # Drag force is split into components
        # Will act in the opposite direction to motion, but motion will change direction so the function will ensure drag force opposite to motion
  drag_force_x = dragForceX(vx)
  drag_force_y  = dragForceY(vy)

        # Overall force
  force_x = drag_force_x
  force_y = drag_force_y + weight
                
        # Acceleration 
  acc_x =  force_x/mass
  acc_y = force_y/mass
                            
        # Calculating new components of velocity
  vx_new = acc_x*dt + vx
  vy_new = acc_y*dt + vy
        
        # Calculating new positions
  rx = rx + vx*dt
  ry_new = ry + vy*dt

        # Changing the direction and reducing the energy if the particle hits the ground        
  if ry_new < 0 and ry >= 0:
    vy_new = -coeff_restitution * vy_new
                        
        # Setting new values to initial variables r_x0, r_y0 and v_y0 to continue the iteration
  ry = ry_new
  vx = vx_new
  vy = vy_new
        
        # Stops the model when the ball is within 1e-5 m of the ground
  if np.isclose(ry,0, atol=(1*(10**-5))):
    break

        
# Calls the ProjectileMotion function to work with these inputs 

with open('test.csv') as csv_file:  # opens the csv file and x1 and y1 will store the co-ordinates for the plot
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)
    x1 = list(np.float_(rows[0]))
    y1 = list(np.float_(rows[1]))


plt.subplots()
plt.plot(x1, y1) # the co-ordinates for the DEM Model are plotted



# naming the x axis
plt.xlabel('Horizontal Displacement')
# naming the y axis
plt.ylabel('Vertical Displacement')
 
# giving a title to my graph
plt.title('Calibrated DEM Model')
plt.gca().invert_yaxis()