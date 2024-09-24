import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# Load JetBrains Mono font
jetbrains_mono = FontProperties(fname="../fonts/JetBrainsMono-Regular.ttf")

# Read the CSV file
df = pd.read_csv('../dataset/lap_2024.csv')

# Calculate average race position for each driver and tire compound
avg_positions = df.groupby(['Driver', 'Compound'])['Position'].mean().reset_index()

# Save the results to a CSV file
avg_positions.to_csv('../csv_generated/average_positions.csv', index=False)

# Create a bar chart
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")
sns.set_palette("deep")

# Create the bar plot
ax = sns.barplot(x='Driver', y='Position', hue='Compound', data=avg_positions)

# Customize the chart
plt.title('Average Race Position by Driver and Tire Compound', fontsize=16, fontweight='bold', fontproperties=jetbrains_mono)
plt.xlabel('Driver', fontsize=12, fontproperties=jetbrains_mono)
plt.ylabel('Average Position', fontsize=12, fontproperties=jetbrains_mono)
plt.xticks(rotation=45, ha='right', fontproperties=jetbrains_mono)
plt.legend(title='Tire Compound', title_fontsize='12', fontsize='10', loc='upper right', frameon=True)

# Set font for tick labels
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(jetbrains_mono)

# Adjust layout and save the chart
plt.tight_layout()
plt.savefig('../charts/tire_compound_analysis.png', dpi=300, bbox_inches='tight')

print("Analysis complete. Results saved to 'average_positions.csv' and 'tire_compound_analysis.png'.")

# Print the font used in the title for verification
print(f"Font used in title: {plt.gca().title.get_fontproperties().get_name()}")