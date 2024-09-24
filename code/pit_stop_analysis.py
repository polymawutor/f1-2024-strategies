import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager

# Add JetBrains Mono font
font_path = '../fonts/JetBrainsMono-Regular.ttf' 
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'JetBrains Mono'

# Read the CSV file
df = pd.read_csv('../dataset/lap_2024.csv', low_memory=False)

# Convert time columns to timedelta
time_columns = ['Time', 'LapTime', 'PitOutTime', 'PitInTime']
for col in time_columns:
    df[col] = pd.to_timedelta(df[col])

# Sort the dataframe by Driver and LapNumber
df = df.sort_values(['Driver', 'LapNumber'])

def calculate_pit_stats(group):
    pit_stops = 0
    pit_times = []
    prev_stint = None
    for i, row in group.iterrows():
        if prev_stint is not None and row['Stint'] != prev_stint:
            pit_stops += 1
            if pd.notnull(group.loc[i-1, 'PitInTime']) and pd.notnull(row['PitOutTime']):
                pit_time = (row['PitOutTime'] - group.loc[i-1, 'PitInTime']).total_seconds()
                if 10 <= pit_time <= 60:  # Reasonable range for pit stop times
                    pit_times.append(pit_time)
        prev_stint = row['Stint']
    
    avg_pit_time = np.mean(pit_times) if pit_times else np.nan
    total_pit_time = np.sum(pit_times)
    
    return pd.Series({
        'PitStops': pit_stops,
        'AvgPitTime': avg_pit_time,
        'TotalPitTime': total_pit_time
    })

# Group by driver and calculate pit stop statistics
# Fix for DeprecationWarning: include_groups=False
pit_stats = df.groupby('Driver', group_keys=False).apply(calculate_pit_stats, include_groups=False).reset_index()

# Save the results to a CSV file
pit_stats.to_csv('../csv_generated/pit_stop_analysis.csv', index=False)

# Filter out rows with NaN values for visualization
pit_stats_filtered = pit_stats.dropna()

# Set the plotting style
# Use a built-in style instead of 'seaborn'
plt.style.use('ggplot')

# Increase the default font size
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

def create_high_quality_chart(data, x, y, title, xlabel, ylabel, filename):
    plt.figure(figsize=(15, 12))  # Increase figure size
    sns.barplot(y=y, x=x, data=data, color='#2C3E50')  # Use a more visually appealing color
    
    plt.title(title, fontsize=20, fontweight='bold')
    plt.ylabel(ylabel, fontsize=16)
    plt.xlabel(xlabel, fontsize=16)
    
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Improve tick label formatting
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.xticks(rotation=0)
    
    # Add value labels to the end of each bar
    for i, v in enumerate(data[x]):
        plt.text(v, i, f' {v:.2f}', va='center', fontsize=10)
    
    plt.tight_layout()
    
    # Save as high-quality PNG and SVG
    plt.savefig(f'../charts/{filename}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'../charts/{filename}.svg', format='svg', bbox_inches='tight')
    
    plt.close()

# Create pit stops chart
pit_stops_sorted = pit_stats_filtered.sort_values('PitStops')
create_high_quality_chart(
    pit_stops_sorted,
    'PitStops',
    'Driver',
    'Number of Pit Stops per Driver',
    'Number of Pit Stops',
    'Driver',
    'pit_stops_per_driver'
)

# Create average time lost chart
avg_time_sorted = pit_stats_filtered.sort_values('AvgPitTime')
create_high_quality_chart(
    avg_time_sorted,
    'AvgPitTime',
    'Driver',
    'Average Time Lost per Pit Stop',
    'Average Time Lost (seconds)',
    'Driver',
    'avg_time_lost_per_pit_stop'
)

print("Analysis complete. High-quality visualizations saved as PNG and SVG files.")