import traci
import numpy as nppip
import csv
import os

# Start SUMO simulation
sumo_cmd = ["sumo", "-c", "sumo_config.sumocfg"]  # Use SUMO-GUI for visualization: ["sumo-gui", "-c", "sumo_config.sumocfg"]
traci.start(sumo_cmd)

# Parameters
collision_threshold = 5.0  # Distance (in meters) to predict collision
communication_range = 50.0  # Communication range in meters

# CSV file setup
output_directory = "dataset_csv"
os.makedirs(output_directory, exist_ok=True)
csv_file_path = os.path.join(output_directory, "vanet_dataset.csv")

# Define CSV headers
csv_headers = ["Vehicle_ID", "X_Position", "Y_Position", "Speed", "Min_Distance", "In_Communication_Range", "Collision_Predicted"]

# Open CSV file for writing
with open(csv_file_path, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_headers)  # Write headers

    def calculate_distance(pos1, pos2):
        """Calculate Euclidean distance between two points."""
        return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    # Simulation loop
    for step in range(500):  # Adjust the number of steps as needed
        traci.simulationStep()  # Advance the simulation by one step
        vehicle_ids = traci.vehicle.getIDList()
       
        for veh_id in vehicle_ids:
            # Extract features for the current vehicle
            pos = traci.vehicle.getPosition(veh_id)
            speed = traci.vehicle.getSpeed(veh_id)
           
            # Calculate distance to the nearest vehicle
            min_distance = float('inf')
            for other_veh_id in vehicle_ids:
                if veh_id != other_veh_id:
                    other_pos = traci.vehicle.getPosition(other_veh_id)
                    distance = calculate_distance(pos, other_pos)
                    if distance < min_distance:
                        min_distance = distance
           
            # Calculate communication range overlap (example feature)
            in_communication_range = min_distance <= communication_range
           
            # Predict collision
            collision_predicted = 1 if min_distance <= collision_threshold else 0
           
            # Write the row to CSV
            csv_writer.writerow([veh_id, pos[0], pos[1], speed, min_distance, int(in_communication_range), collision_predicted])

# Close the simulation
traci.close()

# Print success message
print(f"CSV dataset saved at: {'C:/Users/jlpra/OneDrive/Documents/IDP/IDP2_2024/IDP2_2024'}")
