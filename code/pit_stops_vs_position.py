import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

# Read the CSV files
laps_df = pd.read_csv('../dataset/lap_2024.csv')
results_df = pd.read_csv('../dataset/result_2024.csv')

# Group by Driver and calculate the number of pit stops
pit_stops = laps_df.groupby('Driver')['PitOutTime'].count().reset_index()
pit_stops.columns = ['Driver', 'PitStops']

# Merge pit stops with results
merged_df = results_df.merge(pit_stops, left_on='Abbreviation', right_on='Driver')

# Function to categorize pit stops
def pit_stop_range(stops):
    if stops <= 2:
        return '1-2'
    elif stops <= 4:
        return '3-4'
    else:
        return '5+'

# Add pit stop range column
merged_df['PitStopRange'] = merged_df['PitStops'].apply(pit_stop_range)

# Calculate average final position for each pit stop range
avg_positions = merged_df.groupby('PitStopRange')['Position'].mean().reset_index()

# Save to CSV
avg_positions.to_csv('../csv_generated/pit_stops_vs_position.csv', index=False)

# Set up custom style
plt.style.use('default')
plt.rcParams['axes.facecolor'] = '#E0E0E0'
plt.rcParams['figure.facecolor'] = '#E0E0E0'
plt.rcParams['grid.color'] = 'white'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

# Create scatter plot
plt.figure(figsize=(12, 8))
colors = plt.cm.rainbow(np.linspace(0, 1, len(merged_df)))
scatter = plt.scatter(merged_df['PitStops'], merged_df['Position'], c=colors, s=100, edgecolor='black')

# Customize the plot
plt.title('Pit Stops vs Final Position', fontsize=16, fontweight='bold')
plt.xlabel('Number of Pit Stops', fontsize=12)
plt.ylabel('Final Position', fontsize=12)
plt.gca().invert_yaxis()  # Invert y-axis so that 1st position is at the top
plt.grid(True)

# Use JetBrains Mono font
jetbrains_mono = FontProperties(fname="../fonts/JetBrainsMono-Regular.ttf")
plt.title(plt.gca().get_title(), fontproperties=jetbrains_mono)
plt.xlabel(plt.gca().get_xlabel(), fontproperties=jetbrains_mono)
plt.ylabel(plt.gca().get_ylabel(), fontproperties=jetbrains_mono)
for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
    label.set_fontproperties(jetbrains_mono)

# Add driver abbreviations as labels
for idx, row in merged_df.iterrows():
    plt.annotate(row['Abbreviation'], (row['PitStops'], row['Position']), 
                 xytext=(5, 5), textcoords='offset points', 
                 color='black', fontsize=8, fontweight='bold')

# Add a color bar legend
# cbar = plt.colorbar(scatter, label='Driver', ticks=[])
# cbar.set_ticklabels([])

# Customize color bar
# cbar_labels = merged_df['Abbreviation'].tolist()
# cbar.ax.text(1.5, .5, '\n'.join(cbar_labels), transform=cbar.ax.transAxes, va='center', ha='left', fontsize=8)

# Save the plot
plt.savefig('../charts/pit_stops_vs_position.png', dpi=300, bbox_inches='tight')

print("Analysis complete. Check 'pit_stops_vs_position.csv' for the average positions and 'pit_stops_vs_position.png' for the scatter plot.")