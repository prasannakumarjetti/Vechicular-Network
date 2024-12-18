import pandas as pd
import matplotlib.pyplot as plt

# Load your implementation's simulation data from the CSV file
simulation_data = pd.read_csv('simulation_data.csv')

# Assuming data from paper 1 and paper 2 are stored in variables or CSV files
# Replace these with the actual data from the research papers
paper1_data = {
    'Time (s)': [0, 1000, 2000, 3000, 4000, 5000, 6000],
    'Parking Utilization': [0.1, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9],  # Example data
    'Average Speed (m/s)': [10, 9.5, 9, 8.5, 8, 7.5, 7]  # Example data
}

paper2_data = {
    'Time (s)': [0, 1000, 2000, 3000, 4000, 5000, 6000],
    'Parking Utilization': [0.2, 0.4, 0.6, 0.7, 0.8, 0.85, 0.9],  # Example data
    'Average Speed (m/s)': [10.2, 9.7, 9.2, 8.7, 8.2, 7.7, 7.2]  # Example data
}

# Plot Parking Utilization comparison
plt.figure()
plt.plot(simulation_data['Time (s)'], simulation_data['Parking Utilization'], label='Your Implementation')
plt.plot(paper1_data['Time (s)'], paper1_data['Parking Utilization'], label='Paper 1')
plt.plot(paper2_data['Time (s)'], paper2_data['Parking Utilization'], label='Paper 2')
plt.xlabel('Time (s)')
plt.ylabel('Parking Utilization')
plt.title('Parking Utilization Comparison')
plt.legend()
plt.grid(True)
plt.savefig('parking_utilization_comparison.png')
plt.show()

# Plot Average Speed comparison
plt.figure()
plt.plot(simulation_data['Time (s)'], simulation_data['Average Speed (m/s)'], label='Your Implementation')
plt.plot(paper1_data['Time (s)'], paper1_data['Average Speed (m/s)'], label='Paper 1')
plt.plot(paper2_data['Time (s)'], paper2_data['Average Speed (m/s)'], label='Paper 2')
plt.xlabel('Time (s)')
plt.ylabel('Average Speed (m/s)')
plt.title('Average Speed Comparison')
plt.legend()
plt.grid(True)
plt.savefig('average_speed_comparison.png')
plt.show()
