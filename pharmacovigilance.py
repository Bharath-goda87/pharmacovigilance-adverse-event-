import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = "adverse_events.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError("❌ File not found: adverse_events.csv")

data = pd.read_csv(file_path)

print("=" * 50)
print("Initial Data Preview")
print("=" * 50)
print(data.head())

required_columns = ["Patient_ID", "Drug_Name", "Adverse_Event", "Serious"]

missing_cols = [col for col in required_columns if col not in data.columns]

if missing_cols:
    raise ValueError(f"❌ Missing columns: {missing_cols}")

print("\nColumn validation passed ✅")

print("\nMissing Values:")
print(data.isnull().sum())

print("\n" + "=" * 50)
print("Duplicate Check")
print("=" * 50)

duplicates = data[data.duplicated(
    subset=["Patient_ID", "Drug_Name", "Adverse_Event"],
    keep=False
)]

if not duplicates.empty:
    print("Duplicate Cases Found:")
    print(duplicates)
else:
    print("No duplicate cases found.")

print("Total duplicate records:", len(duplicates))

print("\n" + "=" * 50)
print("Signal Detection")
print("=" * 50)

drug_counts = data["Drug_Name"].value_counts()
print("\nAdverse Event Reports per Drug:")
print(drug_counts)

data["Serious"] = data["Serious"].astype(str).str.strip().str.capitalize()

serious_cases = data[data["Serious"] == "Yes"]

serious_count = (
    serious_cases.groupby(["Drug_Name", "Adverse_Event"])
    .size()
    .reset_index(name="Serious_Count")
)

print("\nPotential Safety Signals (Serious Cases):")
print(serious_count)

expected_events = ["Headache", "Nausea", "Fever", "Fatigue"]

data["Expected"] = data["Adverse_Event"].apply(
    lambda x: "Yes" if x in expected_events else "No"
)

print("\nExpected vs Unexpected:")
print(data["Expected"].value_counts())
signal_threshold = 3
signals = serious_count[serious_count["Serious_Count"] >= signal_threshold]

print("\nPotential Signals:")
print(signals if not signals.empty else "No strong signals detected.")

def classify_reporting(row):
    if row["Serious"] == "Yes" and row["Expected"] == "No":
        return "15-Day Report"
    elif row["Serious"] == "Yes":
        return "Expedited Report"
    else:
        return "Periodic Report"

data["Reporting_Type"] = data.apply(classify_reporting, axis=1)

print("\nGenerating visualizations...")

# Plot 1: Serious vs Non-Serious
plt.figure(figsize=(6, 4))
data["Serious"].value_counts().plot(kind="bar")
plt.title("Serious vs Non-Serious Cases")
plt.xlabel("Case Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("serious_vs_nonserious.png")
plt.close()

event_counts = (
    data.groupby(["Drug_Name", "Adverse_Event"])
    .size()
    .unstack(fill_value=0)
)

plt.figure(figsize=(10, 6))
event_counts.plot(kind="bar", stacked=True)
plt.title("Pharmacovigilance Safety Monitoring")
plt.xlabel("Drug Name")
plt.ylabel("Number of Reports")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("event_distribution.png")
plt.close()

print("✅ Analysis complete. Plots saved.")