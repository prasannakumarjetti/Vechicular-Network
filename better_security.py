import traci
import random
import time
import matplotlib.pyplot as plt
import pandas as pd

# Configuration
SUMO_CONFIG = 'sumo_config.sumocfg'
# Replace with actual lane IDs from your network file
PARKING_SPOTS = ['-251145644#0_0', '-251145644#1_0', '-269696406_0']
PARKING_AREA = 'parking_area'  # Specify the edge or area that represents the parking area

# Simulation Parameters
simulation_time = 600  # total simulation time in seconds
recording_interval = 1  # time interval to record data

# Data Storage
simulation_data = []


def connect_to_sumo():
    """Connect to SUMO using TraCI."""
    traci.start(['sumo', '-c', SUMO_CONFIG])
    print("***Connected to SUMO simulation***")
    print("Available lanes:", traci.lane.getIDList())  # Debug line to print available lanes


def find_available_parking_spot():
    """Find an available parking spot."""
    available_spots = [spot for spot in PARKING_SPOTS if traci.lane.getLastStepVehicleNumber(spot) == 0]
    return random.choice(available_spots) if available_spots else None


def direct_vehicle_to_parking(vehicle_id):
    """Direct the vehicle to the nearest available parking spot."""
    parking_spot = find_available_parking_spot()
    if parking_spot:
        print(f"Directing vehicle {vehicle_id} to parking spot {parking_spot}")
        traci.vehicle.changeTarget(vehicle_id, parking_spot)
        return True  # Successful parking attempt
    else:
        print(f"No available parking spots for vehicle {vehicle_id}")
        return False  # Failed parking attempt


def record_simulation_data(step):
    """Record simulation data at each time step."""
    current_total_vehicles = len(traci.vehicle.getIDList())
    current_parked_vehicles = sum(1 for spot in PARKING_SPOTS if traci.lane.getLastStepVehicleNumber(spot) > 0)
    utilization = current_parked_vehicles / len(PARKING_SPOTS) if PARKING_SPOTS else 0

    # Average speed of vehicles
    speeds = [traci.vehicle.getSpeed(veh) for veh in traci.vehicle.getIDList()]
    current_avg_speed = sum(speeds) / len(speeds) if speeds else 0

    # Waiting times
    waiting_times = [traci.vehicle.getWaitingTime(veh) for veh in traci.vehicle.getIDList()]
    total_waiting_time = sum(waiting_times)
    current_max_waiting_time = max(waiting_times) if waiting_times else 0
    current_min_waiting_time = min(waiting_times) if waiting_times else float('inf')

    # Prepare data to save
    simulation_data.append([
        step, current_total_vehicles, current_parked_vehicles, utilization,
        current_avg_speed, len(waiting_times), total_waiting_time,
        current_max_waiting_time, current_min_waiting_time
    ])


def save_data_to_csv(filename):
    """Save the simulation data to a CSV file."""
    columns = [
        'Time (s)', 'Total Vehicles', 'Parked Vehicles', 'Parking Utilization',
        'Average Speed (m/s)', 'Total Waiting Vehicles', 'Total Waiting Time',
        'Max Waiting Time (s)', 'Min Waiting Time (s)'
    ]
    df = pd.DataFrame(simulation_data, columns=columns)
    df.to_csv(filename, index=False)
    print(f"Simulation data saved to {filename}")


def plot_data(x, y, xlabel, ylabel, title, filename):
    """Plot data and save to a file."""
    plt.figure()
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.savefig(filename)
    plt.close()  # Close the plot to free memory
    print(f"Plot saved as {filename}")


def plot_results():
    """Generate plots from the simulation data."""
    time_steps = [data[0] for data in simulation_data]

    plot_data(time_steps, [data[1] for data in simulation_data], 'Time (s)', 'Total Vehicles',
              'Total Vehicles Over Time', 'total_vehicles.png')
    plot_data(time_steps, [data[2] for data in simulation_data], 'Time (s)', 'Parked Vehicles',
              'Parked Vehicles Over Time', 'parked_vehicles.png')
    plot_data(time_steps, [data[3] for data in simulation_data], 'Time (s)', 'Parking Utilization',
              'Parking Utilization Over Time', 'parking_utilization.png')
    plot_data(time_steps, [data[4] for data in simulation_data], 'Time (s)', 'Average Speed (m/s)',
              'Average Speed Over Time', 'average_speed.png')
    plot_data(time_steps, [data[5] for data in simulation_data], 'Time (s)', 'Total Waiting Vehicles',
              'Total Waiting Vehicles Over Time', 'total_waiting_vehicles.png')
    plot_data(time_steps, [data[6] for data in simulation_data], 'Time (s)', 'Total Waiting Time',
              'Total Waiting Time Over Time', 'total_waiting_time.png')
    plot_data(time_steps, [data[7] for data in simulation_data], 'Time (s)', 'Max Waiting Time (s)',
              'Max Waiting Time Over Time', 'max_waiting_time.png')
    plot_data(time_steps, [data[8] for data in simulation_data], 'Time (s)', 'Min Waiting Time (s)',
              'Min Waiting Time Over Time', 'min_waiting_time.png')


def main():
    connect_to_sumo()
    step = 0

    while step < simulation_time:  # Run the simulation for the defined total simulation time
        traci.simulationStep()

        # Check for vehicles that need to be directed to parking
        for vehicle_id in traci.vehicle.getIDList():
            current_lane = traci.vehicle.getLaneID(vehicle_id)
            print(f"Vehicle {vehicle_id} is in lane {current_lane}")  # Debugging info

            if traci.vehicle.getTypeID(vehicle_id) == 'DEFAULT_VEHTYPE':  # Check for vehicle type
                # Check if vehicle is near the parking area
                if current_lane == PARKING_AREA:  # Adjust this logic if necessary
                    direct_vehicle_to_parking(vehicle_id)

        # Record simulation data at defined intervals
        if step % recording_interval == 0:
            record_simulation_data(step)

        step += 1
        time.sleep(0.1)  # Add a small delay to simulate real-time

    traci.close()
    print("Simulation ended.")

    # Save data to CSV
    save_data_to_csv('simulation_data.csv')

    # Plotting the results after the simulation
    plot_results()


if __name__ == '__main__':
    main()
