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

# Read the CSV files
weather_df = pd.read_csv('../dataset/weather_2024.csv')
lap_df = pd.read_csv('../dataset/lap_2024.csv')

# Convert Time columns to datetime
weather_df['Time'] = pd.to_timedelta(weather_df['Time'])
lap_df['Time'] = pd.to_timedelta(lap_df['Time'])

# Merge the dataframes based on the closest time
merged_df = pd.merge_asof(lap_df.sort_values('Time'), 
                          weather_df.sort_values('Time'), 
                          on='Time', 
                          by='EventName')

# Select relevant columns
output_df = merged_df[['EventName', 'Time', 'Driver', 'Compound', 'AirTemp', 'TrackTemp', 'Humidity', 'Rainfall']]

# Save the results to a CSV file
output_df.to_csv('../csv_generated/weather_tire_analysis.csv', index=False)

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

# Create a scatter plot for Track Temperature vs Tire Compound
fig, ax = plt.subplots(figsize=(15, 12))
sns.scatterplot(data=output_df, x='TrackTemp', y='Compound', hue='Driver', ax=ax, alpha=0.6)
create_high_quality_chart(
    fig, ax,
    'Track Temperature vs Tire Compound',
    'Track Temperature (°C)',
    'Tire Compound',
    'track_temp_vs_compound'
)

# Create a scatter plot for Air Temperature vs Tire Compound
fig, ax = plt.subplots(figsize=(15, 12))
sns.scatterplot(data=output_df, x='AirTemp', y='Compound', hue='Driver', ax=ax, alpha=0.6)
create_high_quality_chart(
    fig, ax,
    'Air Temperature vs Tire Compound',
    'Air Temperature (°C)',
    'Tire Compound',
    'air_temp_vs_compound'
)

# Create a scatter plot for Humidity vs Tire Compound
fig, ax = plt.subplots(figsize=(15, 12))
sns.scatterplot(data=output_df, x='Humidity', y='Compound', hue='Driver', ax=ax, alpha=0.6)
create_high_quality_chart(
    fig, ax,
    'Humidity vs Tire Compound',
    'Humidity (%)',
    'Tire Compound',
    'humidity_vs_compound'
)

print("Analysis complete. Results saved to weather_tire_analysis.csv and charts saved as PNG and SVG files.")