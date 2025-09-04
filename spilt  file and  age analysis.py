import os
import pandas as pd

class PatientDataProcessor:
    """
    Handles splitting file and age analysis for the MIMIC-III patients dataset,
    finding mean age in each parts of the split database file.
     
    Requirments:file forma of, patients.csv.
    The demo files is in the README link
    """

    def __init__(self, filepath: str):
        """
        Initialize with the path to the patients.csv file.
        """
        self.filepath = "eneter file path for patients.csv"
        self.df = self._load_data()
        self.split_dir = os.path.join(os.path.dirname(filepath), "split")
        os.makedirs(self.split_dir, exist_ok=True)

    def _load_data(self) -> pd.DataFrame:
        """
        Load the patients dataset and validate required columns.
        """
        try:
            df = pd.read_csv(self.filepath)
            required_cols = {'subject_id', 'anchor_age'}
            if not required_cols.issubset(df.columns):
                raise ValueError("Missing required columns: 'subject_id', 'anchor_age'")
            return df
        except Exception as e:
            raise RuntimeError(f"Error loading patients data: {e}")

    def split_dataset(self) -> tuple[str, str]:
        """
        Split the dataset into two equal parts and save them as CSV files.
        Returns paths to the split files.
        """
        midpoint = len(self.df) // 2
        df1 = self.df.iloc[:midpoint].copy()
        df2 = self.df.iloc[midpoint:].copy()
        """
        This module Split the dataset into two equal parts, generate two new files\patient_1 and \patient_2
        and save them as CSV files.
        
        """
        path1 = os.path.join(self.split_dir, "enter path to the file, pathpatient_1.csv")
        path2 = os.path.join(self.split_dir, "enter path to the file, pathpatient_2.csv")

        df1.to_csv(path1, index=False)
        df2.to_csv(path2, index=False)

        print(f"✅ Split files saved to:\n→ {path1}\n→ {path2}")
        return path1, path2

    def calculate_mean_age(self, file_path: str) -> float:
        """
        Calculate the mean age from a given split file.
        """
        try:
            df = pd.read_csv(file_path)
            mean_age = df['anchor_age'].mean()
            return round(mean_age, 2)
        except Exception as e:
            raise RuntimeError(f"Error calculating mean age from {file_path}: {e}")

    def run_analysis(self):
        """
        Run the full pipeline: split, analyze, and print results.
        """
        print("📁 Splitting dataset and saving files...")
        file1, file2 = self.split_dataset()

        print("\n📊 Calculating mean age for each split:")
        mean1 = self.calculate_mean_age(file1)
        mean2 = self.calculate_mean_age(file2)
        print(f"→ Mean age in patient_1.csv: {mean1} years")
        print(f"→ Mean age in patient_2.csv: {mean2} years")

        overall_mean = round((mean1 + mean2) / 2, 2)
        print(f"\n🧮 Overall mean age across both splits: {overall_mean} years")


# Example usage
if __name__ == "__main__":
    processor = PatientDataProcessor("patients.csv")
    processor.run_analysis()
