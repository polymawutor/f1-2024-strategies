import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager

# Add JetBrains Mono font
font_path = '../fonts/JetBrainsMono-Regular.ttf' 
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'JetBrains Mono'

# Set the plotting style
plt.style.use('ggplot')

# Increase the default font size
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# Read the CSV file
df = pd.read_csv('../dataset/lap_2024.csv', low_memory=False)

# Convert LapTime to seconds
df['LapTimeSeconds'] = pd.to_timedelta(df['LapTime']).dt.total_seconds()

# Group by Driver and Compound, calculate average lap time and total laps
tire_analysis = df.groupby(['Driver', 'Compound']).agg({
    'LapTimeSeconds': 'mean',
    'LapNumber': 'count'
}).reset_index()

# Rename columns
tire_analysis.columns = ['Driver', 'Compound', 'AverageLapTime', 'TotalLaps']

# Save the results to a CSV file
tire_analysis.to_csv('../csv_generated/tire_compound_analysis.csv', index=False)

def create_high_quality_chart(fig, ax, title, xlabel, ylabel, filename):
    ax.set_title(title, fontsize=20, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.grid(axis='both', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'../charts/{filename}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'../charts/{filename}.svg', format='svg', bbox_inches='tight')
    plt.close(fig)

# Create a box plot to compare lap times across tire compounds
fig, ax = plt.subplots(figsize=(15, 12))
sns.boxplot(x='Compound', y='LapTimeSeconds', data=df, ax=ax)
create_high_quality_chart(
    fig, ax,
    'Lap Times Across Tire Compounds',
    'Compound',
    'Lap Time (seconds)',
    'lap_times_boxplot'
)

# Create a scatter plot showing tire degradation over time
fig, ax = plt.subplots(figsize=(15, 12))
for compound in df['Compound'].unique():
    compound_data = df[df['Compound'] == compound]
    ax.scatter(compound_data['TyreLife'], compound_data['LapTimeSeconds'], 
               label=compound, alpha=0.5)

ax.legend()
create_high_quality_chart(
    fig, ax,
    'Tire Degradation Over Time',
    'Tire Life (laps)',
    'Lap Time (seconds)',
    'tire_degradation_scatter'
)

print("Analysis complete. Results saved to tire_compound_analysis.csv and charts saved as PNG and SVG files.")