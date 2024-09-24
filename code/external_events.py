import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# Read the CSV file
data = pd.read_csv('../csv_generated/external_events.csv', index_col=0)

# Replace empty strings with NaN and convert to float
data = data.replace('', pd.NA).astype(float)

# Sort drivers by their average lap time (using GREEN_True as a baseline)
driver_order = data['GREEN_True'].sort_values().index

# Create a heatmap
plt.figure(figsize=(20, 12))
sns.heatmap(data.loc[driver_order], annot=True, fmt='.2f', cmap='YlOrRd', 
            linewidths=0.5, cbar_kws={'label': 'Average Lap Time (seconds)'})

# Customize the plot
plt.title('Average Lap Times Under Different Conditions', fontsize=16)
plt.xlabel('Conditions', fontsize=12)
plt.ylabel('Drivers', fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Apply JetBrains Mono font
jetbrains_mono = FontProperties(fname="../fonts/JetBrainsMono-Regular.ttf")
plt.title(plt.gca().get_title(), fontproperties=jetbrains_mono)
plt.xlabel(plt.gca().get_xlabel(), fontproperties=jetbrains_mono)
plt.ylabel(plt.gca().get_ylabel(), fontproperties=jetbrains_mono)
for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
    label.set_fontproperties(jetbrains_mono)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig('../charts/lap_times_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("Heatmap visualization complete. Results saved to 'lap_times_heatmap.png'.")