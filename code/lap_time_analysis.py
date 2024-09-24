import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.font_manager import FontProperties

# Read the lap data CSV file
lap_df = pd.read_csv('../dataset/lap_2024.csv')

# Convert LapTime to seconds
def lap_time_to_seconds(lap_time):
    if pd.isna(lap_time):
        return np.nan
    if isinstance(lap_time, str):
        time_str = lap_time.split(' ', 2)[-1]
        hours, minutes, seconds = time_str.split(':')
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    elif isinstance(lap_time, (int, float)):
        return lap_time
    else:
        return np.nan

lap_df['LapTimeSeconds'] = lap_df['LapTime'].apply(lap_time_to_seconds)

# Calculate average lap time for each driver across all events
driver_averages = lap_df.groupby('Driver')['LapTimeSeconds'].mean().sort_values()

# Set up the plot
plt.figure(figsize=(15, 10))
sns.set_style("whitegrid")

# Load JetBrains Mono font
jetbrains_mono = FontProperties(fname="../fonts/JetBrainsMono-Regular.ttf")

# Create bar plot
bar_plot = sns.barplot(x=driver_averages.index, y=driver_averages.values, color="black")

# Customize the plot
plt.xlabel('Drivers', fontproperties=jetbrains_mono, fontsize=12)
plt.ylabel('Average Lap Time (seconds)', fontproperties=jetbrains_mono, fontsize=12)
plt.title('Average Lap Time by Driver - All Grand Prix', fontproperties=jetbrains_mono, fontsize=16)
plt.xticks(rotation=45, ha='right', fontproperties=jetbrains_mono)
plt.yticks(fontproperties=jetbrains_mono)

# Add value labels on top of each bar
for i, v in enumerate(driver_averages.values):
    bar_plot.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontproperties=jetbrains_mono, fontsize=8)

plt.tight_layout()

# Save the chart
plt.savefig('../charts/driver_average_lap_time_chart.png', dpi=300, bbox_inches='tight')
plt.close()

# Prepare and save CSV output
output_df = pd.DataFrame({
    'Driver': driver_averages.index,
    'AverageLapTime': driver_averages.values
})
output_df.to_csv('../csv_generated/driver_average_lap_times.csv', index=False)

print("Driver average lap time chart created and saved as 'driver_average_lap_time_chart.png'.")
print("Driver average lap time data saved as 'driver_average_lap_times.csv'.")