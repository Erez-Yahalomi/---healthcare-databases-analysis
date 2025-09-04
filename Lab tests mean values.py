
 
import pandas as pd

class LabStatsAnalyzer:
    """
    Analyzes lab test statistics -  mean value of the results on the database, for each type of test
    by joining lab definitions with lab events.

    Requirments:file formats of, 1. d_labitems.csv. 2. labevents.csv.
    Demo files are in the README link
    """

    def __init__(self, labitems_path: str, labevents_path: str):
        """
        Initialize with paths to lab definitions and lab events CSV files.
        """
        self.labitems_path = "enter full path for d_labitems.csv"  
        self.labevents_path = "enter full path for labevents.csv"  
        self.labitems_df = self._load_labitems()
        self.labevents_df = self._load_labevents()

    def _load_labitems(self) -> pd.DataFrame:
        """
        Load lab definitions (d_labitems.csv).
        """
        try:
            df = pd.read_csv(self.labitems_path)
            if 'itemid' not in df.columns or 'label' not in df.columns:
                raise ValueError("Missing required columns in labitems.")
            return df
        except Exception as e:
            raise RuntimeError(f"Error loading labitems: {e}")

    def _load_labevents(self) -> pd.DataFrame:
        """
        Load lab measurements (labevents.csv).
        """
        try:
            df = pd.read_csv(self.labevents_path)
            if 'itemid' not in df.columns or 'value' not in df.columns:
                raise ValueError("Missing required columns in labevents.")
            return df
        except Exception as e:
            raise RuntimeError(f"Error loading labevents: {e}")

    def compute_statistics(self) -> pd.DataFrame:
        """
        Join labitems with labevents and compute mean and missing percentage per label.
        """
        # Merge lab definitions with measurements
        merged_df = pd.merge(
            self.labevents_df,
            self.labitems_df[['itemid', 'label']],
            on='itemid',
            how='left'
        )

        # Group by label and compute statistics
        stats_df = (
            merged_df
            .groupby('label')
            .agg(
                mean_value=('value', lambda x: pd.to_numeric(x, errors='coerce').mean()),
                missing_percent=('value', lambda x: x.isnull().mean() * 100)
            )
            .reset_index()
        )

        # Round results for readability
        stats_df['mean_value'] = stats_df['mean_value'].round(2)
        stats_df['missing_percent'] = stats_df['missing_percent'].round(2)

        return stats_df

    def run_analysis(self):
        """
        Execute the analysis and print the results.
        """
        print("📊 Lab Test Statistics by Label:\n")
        stats = self.compute_statistics()
        print(stats.to_string(index=False))


# Example usage
if __name__ == "__main__":
    analyzer = LabStatsAnalyzer("d_labitems.csv", "labevents.csv")
    analyzer.run_analysis()


""""
tep-by-Step Complexity Analysis
1. Loading CSV Files
python
pd.read_csv(...)
Time Complexity: O(n) for labevents, O(m) for d_labitems

Each row is read once → linear time

2. Merging labitems with labevents
python
pd.merge(labevents_df, labitems_df[['itemid', 'label']], on='itemid', how='left')
Time Complexity: O(n + m)

Merge operation is linear in both datasets assuming hash-based join

3. Grouping by Label
python
groupby('label')
Time Complexity: O(n)

Each row is assigned to a group based on its label

4. Aggregation: Mean and Missing Percent
python
agg(mean_value, missing_percent)
Time Complexity: O(n)

Each group computes:

Mean: O(k) where k is group size

Missing percent: O(k)

Total across all groups: still O(n)



Combining all steps:

O(n + m)

This is efficient and scales linearly with the size of the input files. The dominant factor is the number of lab measurement records (n), 
which can be in the millions in MIMIC-III.
"""
