import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Read the CSV file
df = pd.read_csv('../dataset/lap_2024.csv')

# Convert LapTime to seconds
df['LapTime'] = pd.to_timedelta(df['LapTime']).dt.total_seconds()

# Group by Compound and TyreLife, and calculate average lap time
grouped = df.groupby(['Compound', 'TyreLife'])['LapTime'].mean().reset_index()

# Calculate delta time for each compound
compounds = grouped['Compound'].unique()
delta_data = []

for compound in compounds:
    compound_data = grouped[grouped['Compound'] == compound].sort_values('TyreLife')
    base_time = compound_data['LapTime'].iloc[0]
    compound_data['DeltaTime'] = compound_data['LapTime'] - base_time
    delta_data.append(compound_data)

delta_df = pd.concat(delta_data)

# Calculate average delta time for each compound and lap
avg_delta = delta_df.groupby(['Compound', 'TyreLife'])['DeltaTime'].mean().reset_index()

# Pivot the data for easier plotting
pivot_data = avg_delta.pivot(index='TyreLife', columns='Compound', values='DeltaTime')

# Create the line graph
plt.figure(figsize=(12, 8))
for compound in pivot_data.columns:
    plt.plot(pivot_data.index, pivot_data[compound], label=compound, linewidth=2)

# Customize the chart
plt.title('Average Delta Time vs Tire Life by Compound', fontsize=16, fontweight='bold')
plt.xlabel('Tire Life (Laps)', fontsize=12)
plt.ylabel('Average Delta Time (seconds)', fontsize=12)
plt.legend(title='Tire Compound', title_fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Set JetBrains Mono font
jetbrains_mono = FontProperties(fname="../fonts/JetBrainsMono-Regular.ttf")
plt.title(plt.gca().get_title(), fontproperties=jetbrains_mono)
plt.xlabel(plt.gca().get_xlabel(), fontproperties=jetbrains_mono)
plt.ylabel(plt.gca().get_ylabel(), fontproperties=jetbrains_mono)
for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
    label.set_fontproperties(jetbrains_mono)

# Set colors
plt.gca().set_facecolor('white')
for spine in plt.gca().spines.values():
    spine.set_edgecolor('black')

# Save the chart
plt.tight_layout()
plt.savefig('../charts/tire_delta_analysis_chart.png', dpi=300, bbox_inches='tight')
plt.close()

# Prepare data for CSV output
csv_data = avg_delta.groupby('Compound').agg({
    'TyreLife': 'max',
    'DeltaTime': 'mean'
}).reset_index()
csv_data.columns = ['TireCompound', 'Laps', 'AvgDeltaTime']
csv_data.to_csv('../csv_generated/tire_delta_analysis.csv', index=False)

print("Analysis complete. Results saved to 'tire_delta_analysis.csv' and 'tire_delta_analysis_chart.png'.")