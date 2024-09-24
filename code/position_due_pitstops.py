import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D
from datetime import timedelta

def parse_custom_time(time_str):
    if pd.isna(time_str):
        return pd.NaT
    try:
        days, time = time_str.split(' days ')
        hours, minutes, seconds = time.split(':')
        seconds, microseconds = seconds.split('.')
        
        return timedelta(
            days=int(days),
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds),
            microseconds=int(microseconds)
        )
    except ValueError:
        return pd.NaT

# Read the CSV files
position_df = pd.read_csv('../dataset/position_2O24.csv', low_memory=False)
lap_df = pd.read_csv('../dataset/lap_2024.csv', low_memory=False)

# Convert Time columns to timedelta
position_df['Time'] = position_df['Time'].apply(parse_custom_time)
lap_df['Time'] = lap_df['Time'].apply(parse_custom_time)

# Calculate the race start time
race_start = position_df['Time'].min()

# Convert timedelta to seconds since race start
position_df['Seconds'] = (position_df['Time'] - race_start).dt.total_seconds()
lap_df['Seconds'] = (lap_df['Time'] - race_start).dt.total_seconds()

# Calculate position for each driver at each time point
position_df = position_df.sort_values('Seconds')
position_df['Position'] = position_df.groupby('Seconds')['DriverName'].rank(method='dense')

# Identify pit stops
pit_stops = lap_df[lap_df['PitInTime'].notna()]

# Initialize lists to store data for CSV
csv_data = []

# Process each driver's data
for driver in position_df['DriverName'].unique():
    driver_positions = position_df[position_df['DriverName'] == driver].sort_values('Seconds')
    driver_pit_stops = pit_stops[pit_stops['Driver'] == driver]
    
    for _, pit_stop in driver_pit_stops.iterrows():
        pit_time = pit_stop['Seconds']
        before_pit = driver_positions[driver_positions['Seconds'] < pit_time]['Position'].iloc[-1] if not driver_positions[driver_positions['Seconds'] < pit_time].empty else None
        after_pit = driver_positions[driver_positions['Seconds'] > pit_time]['Position'].iloc[0] if not driver_positions[driver_positions['Seconds'] > pit_time].empty else None
        
        if before_pit is not None and after_pit is not None:
            position_change = before_pit - after_pit
            csv_data.append({
                'Driver': driver,
                'PitStopTime': pit_time / 3600,  # Convert to hours
                'PositionBefore': before_pit,
                'PositionAfter': after_pit,
                'PositionChange': position_change
            })

# Create a CSV file with position changes
csv_df = pd.DataFrame(csv_data)
csv_df.to_csv('../csv_generated/position_changes.csv', index=False)

# Create a simplified line chart showing position changes
plt.figure(figsize=(15, 10))
plt.style.use('default')  # Use default style for white background

# Add JetBrains Mono font
font_path = '../fonts/JetBrainsMono-Regular.ttf'  # Update this path
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

# Color palette for drivers
color_palette = plt.cm.get_cmap('tab20')

for idx, driver in enumerate(position_df['DriverName'].unique()):
    driver_data = position_df[position_df['DriverName'] == driver].sort_values('Seconds')
    plt.plot(driver_data['Seconds'] / 3600, driver_data['Position'], 
             label=driver, color=color_palette(idx / 20), linewidth=2)

    # Mark pit stops
    driver_pit_stops = pit_stops[pit_stops['Driver'] == driver]
    for pit_time in driver_pit_stops['Seconds']:
        plt.plot(pit_time / 3600, driver_data[driver_data['Seconds'] >= pit_time]['Position'].iloc[0], 
                 'o', color=color_palette(idx / 20), markersize=8)

plt.gca().invert_yaxis()  # Invert y-axis so that position 1 is at the top
plt.xlabel('Time (hours from race start)', fontproperties=prop, fontsize=12)
plt.ylabel('Position', fontproperties=prop, fontsize=12)
plt.title('Driver Positions Throughout the Race', fontproperties=prop, fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(prop=prop, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

# Customize ticks
plt.xticks(fontproperties=prop, fontsize=10)
plt.yticks(range(1, len(position_df['DriverName'].unique()) + 1), fontproperties=prop, fontsize=10)

plt.tight_layout()
plt.savefig('../charts/position_changes.png', dpi=300, bbox_inches='tight')
plt.close()

print("Analysis complete. Results saved in 'position_changes.csv' and 'simplified_position_changes.png'.")