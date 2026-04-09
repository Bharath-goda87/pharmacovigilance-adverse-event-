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
        print(f"Missing values found in {col}")
    else:
        print(f"{col} validated successfully")

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

serious_count = serious_cases.groupby(
    ["Drug_Name","Adverse_Event"]
).size().reset_index(name="Serious_Count")

print("\nPotential Safety Signals (Serious Cases):")
print(serious_count)

data["Expected"] = ["Yes" if x in ["Headache", "Nausea"] else "No" for x in data["Adverse_Event"]]

expected_counts = data["Expected"].value_counts()
print("\nExpected vs Unexpected:")
print(expected_counts)

signal_threshold = 3

signals = serious_count[serious_count["Serious_Count"] >= signal_threshold]

print("\nPotential Signals:")
print(signals)

def classify_reporting(row):
    if row["Serious"] == "Yes" and row["Expected"] == "No":
        return "15-Day Report"
    elif row["Serious"] == "Yes":
        return "Expedited Report"
    else:
        return "Periodic Report"

data["Reporting_Type"] = data.apply(classify_reporting, axis=1)

serious_summary = data["Serious"].value_counts()

plt.figure()
serious_summary.plot(kind="bar")
plt.title("Serious vs Non-Serious Cases")
plt.xlabel("Case Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("serious_vs_nonserious.png")
plt.close()

event_counts = data.groupby(
    ["Drug_Name", "Adverse_Event"]
).size().unstack(fill_value=0)

plt.figure()
event_counts.plot(kind="bar", stacked=True)
plt.title("Pharmacovigilance Safety Monitoring")
plt.xlabel("Drug Name")
plt.ylabel("Number of Reports")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("event_distribution.png")
plt.close()

