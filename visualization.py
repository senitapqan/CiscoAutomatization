import csv
import matplotlib.pyplot as plt

# Read CSV file into a list of rows
csv_file_path = 'C:\\Users\\77782\Desktop\SDU\\3 course\cisco\\finalProject\csv\\result.csv'
with open(csv_file_path, 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)  # Assuming the first row contains headers
    data = [row for row in csvreader]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(8, 4))

# Hide the axes
ax.axis('off')

# Create a table
table = ax.table(cellText=[headers] + data,
                 colLabels=None,
                 cellLoc='center',
                 loc='center')

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)  # Adjust the table size

plt.title('CSV Data as Table')
plt.show()
