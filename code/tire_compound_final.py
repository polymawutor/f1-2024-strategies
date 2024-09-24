import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Read the CSV files
result_df = pd.read_csv('../dataset/result_2024.csv')
lap_df = pd.read_csv('../dataset/lap_2024.csv')

# Convert ClassifiedPosition to numeric, replacing any non-numeric values with NaN
result_df['ClassifiedPosition'] = pd.to_numeric(result_df['ClassifiedPosition'], errors='coerce')

# Merge the dataframes to get starting tire information
merged_df = pd.merge(result_df, lap_df[lap_df['LapNumber'] == 1][['DriverNumber', 'Compound']], 
                     on='DriverNumber', how='left')

# Calculate average final position for each tire compound
tire_avg_position = merged_df.groupby('Compound')['ClassifiedPosition'].mean().reset_index()

# Sort by average position (ascending order)
tire_avg_position = tire_avg_position.sort_values('ClassifiedPosition')

# Save to CSV
tire_avg_position.to_csv('../csv_generated/tire_average_position.csv', index=False, 
                         columns=['Compound', 'ClassifiedPosition'])

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(tire_avg_position['Compound'], tire_avg_position['ClassifiedPosition'], 
        color='black', edgecolor='white')

# Customize the chart
plt.title('Average Final Position by Starting Tire Compound', fontsize=16, fontweight='bold')
plt.xlabel('Tire Compound', fontsize=12)
plt.ylabel('Average Final Position', fontsize=12)
plt.gca().invert_yaxis()  # Invert y-axis so lower positions (better) are higher on the chart

# Set JetBrains Mono font
jetbrains_mono = FontProperties(fname="../fonts/JetBrainsMono-Regular.ttf")
plt.title(plt.gca().get_title(), fontproperties=jetbrains_mono)
plt.xlabel(plt.gca().get_xlabel(), fontproperties=jetbrains_mono)
plt.ylabel(plt.gca().get_ylabel(), fontproperties=jetbrains_mono)
for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
    label.set_fontproperties(jetbrains_mono)

# Add value labels on top of each bar
for i, v in enumerate(tire_avg_position['ClassifiedPosition']):
    plt.text(i, v, f'{v:.2f}', ha='center', va='bottom')

# Set background color to white
plt.gca().set_facecolor('white')

# Remove top and right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Save the chart
plt.tight_layout()
plt.savefig('../charts/tire_average_position_chart.png', dpi=300, bbox_inches='tight')
plt.close()

print("Analysis complete. Results saved to 'tire_average_position.csv' and 'tire_average_position_chart.png'.")