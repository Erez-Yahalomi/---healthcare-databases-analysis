"""
This script is used to calculate the mean and median age of the patients in the dataset.

Use the format of MIMIC, patients, database file. Link to demo database files is in the README.
"""

import pandas as pd
file_path = "write full path here"
# Load dataset
df = pd.read_csv(file_path)


# Apply rule: ages > 89 → set to 91
df["age"] = df["anchor_age"].clip(upper=89).replace(89, 91)

# Compute stats
mean_age = df["age"].mean()
median_age = df["age"].median()

print(f"Average age: {mean_age:.2f}")
print(f"Median age: {median_age:.2f}")
