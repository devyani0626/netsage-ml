
import pandas as pd

data = pd.read_csv("data/network_cases.csv")

print("Dataset shape:", data.shape)

print("\nClass distribution:")
print(data["fault"].value_counts())

print("\nDuplicate rows:")
duplicates = data[data.duplicated(keep=False)]
print(duplicates.sort_values(by=list(data.columns)).to_string(index=False))

print("\nUnique feature combinations:")
print(data.drop(columns=["fault"]).drop_duplicates().shape[0])
