
import pandas as pd

data = pd.read_csv("data/network_cases.csv")

print("Original dataset:", data.shape)

# Remove rows that are identical in every column
cleaned = data.drop_duplicates().reset_index(drop=True)

print("After removing exact duplicates:", cleaned.shape)

print("\nClass distribution:")
print(cleaned["fault"].value_counts())

print("\nCleaned dataset:")
print(cleaned.to_string(index=False))

cleaned.to_csv("data/network_cases_cleaned.csv", index=False)

print("\nSaved to data/network_cases_cleaned.csv")
