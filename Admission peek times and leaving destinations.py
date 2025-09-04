
"""
This module:
1. Identify peak admission times.
Aggregates admissions by hour and day of week.
Presenting output by histograms for identifying
highlights Peak admission times, for staffing optimization

2. Analyze discharge destinations, Groups by discharge_location
Shows volume and percentage of discharges to each destination.

 Requirments, file formats of admissions.csv.
 Demo files are in the README link
"""


import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Optional


class AdmissionsAnalyzer:
    def __init__(self, admissions_df: pd.DataFrame):
        self.df = admissions_df.copy()
        self._prepare_data()

    def _prepare_data(self):
        """Convert admittime to datetime and extract hour/day features."""
        self.df["admittime"] = pd.to_datetime(self.df["admittime"], errors="coerce")
        self.df.dropna(subset=["admittime"], inplace=True)
        self.df["hour"] = self.df["admittime"].dt.hour
        self.df["day_of_week"] = self.df["admittime"].dt.day_name()

    def peak_admission_times(self) -> pd.DataFrame:
        """Return admission counts by hour and day of week."""
        hourly = self.df.groupby("hour").size().reset_index(name="admissions")
        daily = self.df.groupby("day_of_week").size().reset_index(name="admissions")

        # Sort days in calendar order
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        daily["day_of_week"] = pd.Categorical(daily["day_of_week"], categories=day_order, ordered=True)
        daily = daily.sort_values("day_of_week")

        return hourly, daily

    def plot_peak_admission_times(self):
        """Generate bar charts for admissions by hour and day of week."""
        hourly, daily = self.peak_admission_times()

        # Bar chart: Admissions by Hour
        plt.figure(figsize=(10, 5))
        plt.bar(hourly["hour"], hourly["admissions"], color="skyblue")
        plt.title("📈 Admissions by Hour")
        plt.xlabel("Hour of Day")
        plt.ylabel("Number of Admissions")
        plt.xticks(range(0, 24))
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Bar chart: Admissions by Day of Week
        plt.figure(figsize=(10, 5))
        plt.bar(daily["day_of_week"], daily["admissions"], color="salmon")
        plt.title("📅 Admissions by Day of Week")
        plt.xlabel("Day")
        plt.ylabel("Number of Admissions")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()

    def discharge_destination_summary(self) -> pd.DataFrame:
        """Return discharge location counts and percentages."""
        discharge_counts = (
            self.df["discharge_location"]
            .fillna("UNKNOWN")
            .value_counts()
            .reset_index()
        )
        discharge_counts.columns = ["discharge_location", "count"]
        discharge_counts["percent"] = (
            discharge_counts["count"] / discharge_counts["count"].sum() * 100
        ).round(2)
        return discharge_counts


# Example usage
if __name__ == "__main__":
    path = "enter full path for, admissions.csv"
    df = pd.read_csv(path)
    analyzer = AdmissionsAnalyzer(df)

    # Show bar charts for staffing optimization
    analyzer.plot_peak_admission_times()

    # Optional: print discharge summary
    discharge_summary = analyzer.discharge_destination_summary()
    print("\n🏥 Discharge Destination Summary:\n", discharge_summary)
