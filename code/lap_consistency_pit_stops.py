import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Read the lap data
lap_data = pd.read_csv('../dataset/lap_2024.csv', parse_dates=['Time', 'LapStartDate'])

# Convert LapTime to seconds
lap_data['LapTimeSeconds'] = pd.to_timedelta(lap_data['LapTime']).dt.total_seconds()

# Function to detect pit stops
def detect_pit_stops(group):
    pit_stops = (group['Stint'] != group['Stint'].shift()).sum() - 1
    return pd.Series({'PitStops': pit_stops})

# Calculate statistics for each driver
driver_stats = lap_data.groupby('Driver').agg({
    'LapTimeSeconds': ['std', 'count'],
    'Stint': 'max'
})

driver_stats.columns = ['LapTimeStd', 'TotalLaps', 'MaxStint']

# Calculate number of pit stops
pit_stops = lap_data.groupby('Driver').apply(detect_pit_stops)
driver_stats = driver_stats.join(pit_stops)

# Calculate average stint length
driver_stats['AvgStintLength'] = driver_stats['TotalLaps'] / (driver_stats['PitStops'] + 1)

# Save results to CSV
driver_stats.to_csv('../csv_generated/lap_consistency_pit_stops.csv')

# Create scatter plot
plt.figure(figsize=(12, 8))
plt.scatter(driver_stats['LapTimeStd'], driver_stats['PitStops'], 
            c='white', edgecolors='black', s=50)

# Add driver labels
for idx, row in driver_stats.iterrows():
    plt.annotate(idx, (row['LapTimeStd'], row['PitStops']), 
                 xytext=(5, 5), textcoords='offset points', 
                 fontsize=8, color='white')

# Customize the plot
plt.title('Lap Time Consistency vs Number of Pit Stops', fontsize=16, color='white')
plt.xlabel('Lap Time Standard Deviation (seconds)', fontsize=12, color='white')
plt.ylabel('Number of Pit Stops', fontsize=12, color='white')
plt.grid(True, linestyle='--', alpha=0.7)

# Set black background
plt.gca().set_facecolor('black')
plt.gcf().set_facecolor('black')

# Customize tick colors
plt.tick_params(colors='white')

# Apply JetBrains Mono font
jetbrains_mono = FontProperties(fname="../fonts/JetBrainsMono-Regular.ttf")
plt.gca().set_xticklabels(plt.gca().get_xticks(), fontproperties=jetbrains_mono)
plt.gca().set_yticklabels(plt.gca().get_yticks(), fontproperties=jetbrains_mono)
plt.title(plt.gca().get_title(), fontproperties=jetbrains_mono)
plt.xlabel(plt.gca().get_xlabel(), fontproperties=jetbrains_mono)
plt.ylabel(plt.gca().get_ylabel(), fontproperties=jetbrains_mono)

# Save the plot
plt.tight_layout()
plt.savefig('../charts/lap_time_consistency_vs_pit_stops.png', dpi=300, bbox_inches='tight')
plt.close()

print("Analysis complete. Results saved to 'driver_statistics.csv' and 'lap_time_consistency_vs_pit_stops.png'.")