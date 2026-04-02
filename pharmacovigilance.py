import pandas as pd
import matplotlib.pyplot as plt
import os
file_path = "adverse_events.csv"

if not os.path.exists(file_path):
    print("File not found. Please make sure adverse_events.csv is in same folder.")
    exit()

data = pd.read_csv(file_path)
print(40*"==")
print("Initial Data Preview")
print(2*"====================================")
print(data.head())
print(2*"\n====================================")
print("Case Validation")
print(2*"====================================")

print("\nMissing Values:")
print(data.isnull().sum())

required_columns = ["Patient_ID", "Drug_Name", "Adverse_Event"]

for col in required_columns:
    if data[col].isnull().any():
        print(f"❌ Missing values found in {col}")
    else:
        print(f"✅ {col} validated successfully")
print("\nCase validation completed.")
print(2*"\n====================================")
print("Duplicate Check")
print(2*"====================================")

duplicates = data[data.duplicated(
    subset=["Patient_ID", "Drug_Name", "Adverse_Event"],
    keep=False
)]
if len(duplicates) > 0:
    print("Duplicate Cases Found:")
    print(duplicates)
else:
    print("No duplicate cases found.")

print("Total duplicate records:", len(duplicates))
print(2*"\n====================================")
print("Signal Detection")
print(2*"====================================")
drug_counts = data["Drug_Name"].value_counts()
print("\nAdverse Event Reports per Drug:")
print(drug_counts)
serious_cases = data[data["Serious"] == "Yes"]
serious_count = serious_cases.groupby(["Drug_Name","Adverse_Event"]).size().reset_index(name="Serious_Count")
print("\nPotential Safety Signals (Serious Cases):")
print(serious_count)
event_counts = data.groupby(
    ["Drug_Name", "Adverse_Event"]
).size().unstack(fill_value=0)
plt.figure(figsize=(12,7)) 
event_counts.plot(
    kind="bar",
    stacked=True,
    figsize=(12,7)
)
plt.title(" Pharmacovigilance Safety Monitoring Project", fontsize=25,color="blue")
plt.xlabel("Drug Name", fontsize=15,color="blue")
plt.ylabel("Number of Reports", fontsize=15,color="blue")
plt.xticks(rotation=45, ha="right")  
plt.legend(title="Adverse Event", bbox_to_anchor=(1.05,1))  
plt.tight_layout()
plt.savefig("event_distribution.png")
plt.show()
print("This data saved in the event distribution.png")