import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from collections import Counter

# Load the data
lap_data = pd.read_csv('../dataset/lap_2024.csv')

# Group by EventName and Driver
grouped = lap_data.groupby(['EventName', 'Driver'])

# Calculate statistics
race_stats = []
for (event, driver), group in grouped:
    total_laps = group['LapNumber'].max()
    pit_stops = group['Stint'].nunique() - 1  # Subtract 1 because the first stint doesn't count as a pit stop
    tire_choices = group['Compound'].value_counts().index[0]  # Most common tire
    race_stats.append({
        'EventName': event,
        'Driver': driver,
        'TotalLaps': total_laps,
        'PitStops': pit_stops,
        'MostCommonTire': tire_choices
    })

race_stats_df = pd.DataFrame(race_stats)

# Calculate averages by race length
race_length_stats = race_stats_df.groupby('TotalLaps').agg({
    'PitStops': 'mean',
    'MostCommonTire': lambda x: Counter(x).most_common(1)[0][0]
}).reset_index()

race_length_stats.columns = ['RaceLength', 'AvgPitStops', 'MostCommonTire']

# Save to CSV
race_length_stats.to_csv('../csv_generated/race_length_stats.csv', index=False)

# Plotting
plt.figure(figsize=(12, 8))
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['JetBrains Mono']

jetbrains_mono = FontProperties(fname="../fonts/JetBrainsMono-Regular.ttf")
plt.title(plt.gca().get_title(), fontproperties=jetbrains_mono)
plt.xlabel(plt.gca().get_xlabel(), fontproperties=jetbrains_mono)
plt.ylabel(plt.gca().get_ylabel(), fontproperties=jetbrains_mono)
for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
    label.set_fontproperties(jetbrains_mono)

# # Set the style and color palette
# plt.style.use('dark_background')
# sns.set_palette("husl")

# Create a scatter plot
for tire in race_length_stats['MostCommonTire'].unique():
    data = race_length_stats[race_length_stats['MostCommonTire'] == tire]
    plt.scatter(data['RaceLength'], data['AvgPitStops'], 
                label=tire, s=100, alpha=0.7)

plt.xlabel('Race Length (Laps)', fontproperties=jetbrains_mono)
plt.ylabel('Average Number of Pit Stops', fontproperties=jetbrains_mono)
plt.title('Pit Stops vs Race Length by Most Common Tire', fontproperties=jetbrains_mono)
plt.legend(prop=jetbrains_mono, title="Most Common Tire")

# Customize the plot
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot
plt.savefig('../charts/race_analysis_plot_improved.png', facecolor='white', edgecolor='none')
plt.close()

print("Analysis complete. Results saved to 'race_length_stats.csv' and 'race_analysis_plot_improved.png'.")