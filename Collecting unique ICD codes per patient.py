import pandas as pd

class ICDAnalyzer:
    """
    A class to analyze ICD codes from the MIMIC-III diagnoses dataset.
    Collecting all ICD codes of each patient from a disordered database and export it to a csv file where each patient (subject_id)
    has a raw listing all of his ICD codes Requirements MIMIC 1. diagnoses_icd.csv database. 2. unique_icd_per_patient.csv database file
    Demo database files are in the MIMIC link in README

    This class also returns the top N ICD codes and their percentage of total ICD code occurrences in the database.
    """

    def __init__(self, filepath: str):
        """
        Initialize the analyzer with the path to the CSV file.
        """
        filepath = "enter here the full path to diagnoses_icd.csv file" 
        self.filepath = filepath
        self.df = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        """
        Load the CSV file into a pandas DataFrame.
        """
        try:
            df = pd.read_csv(self.filepath)
            required_cols = {'subject_id', 'icd_code'}
            if not required_cols.issubset(df.columns):
                raise ValueError("Missing required columns in dataset.")
            return df
        except Exception as e:
            raise RuntimeError(f"Failed to load data: {e}")

    def get_unique_icd_per_patient(self) -> pd.DataFrame:
        """
        Returns a DataFrame with one row per subject_id and a list of unique ICD codes.
        """
        unique_icd = self.df.groupby('subject_id')['icd_code'].unique().reset_index()
        unique_icd['unique_icd_count'] = unique_icd['icd_code'].apply(len)
        return unique_icd

    def export_unique_icd_to_csv(self, output_path: str):
        """
        Exports the unique ICD codes per subject_id to a CSV file.
        """
        unique_icd_df = self.get_unique_icd_per_patient()

        # Convert list of ICD codes to a comma-separated string for CSV readability
        unique_icd_df['icd_code'] = unique_icd_df['icd_code'].apply(lambda codes: ', '.join(codes))

        # Save to CSV
        output_path = "enter here the full path to the file, unique_icd_per_patient.csv" 
        unique_icd_df.to_csv(output_path, index=False)
        print(f"✅ Unique ICD codes per patient exported to: {output_path}")

    def run_analysis(self):
        """
        Run all analyses and print results.
        """
        print("🔍 Average number of unique ICD codes per patient:")
        avg_icd = self.get_unique_icd_per_patient()['unique_icd_count'].mean()
        print(f"→ {round(avg_icd, 2)} ICD codes per patient on average\n")

        print("📁 Exporting unique ICD codes per patient to CSV...")
        self.export_unique_icd_to_csv("unique_icd_per_patient.csv")

        print("\n🔥 Top 10 ICD codes and their percentage of total:")
        top_icd_df = self.get_top_icd_codes()
        print(top_icd_df)

    def get_top_icd_codes(self, top_n: int = 10) -> pd.DataFrame:
        """
        Returns the top N ICD codes and their percentage of total ICD code occurrences.
        """
        icd_counts = self.df['icd_code'].value_counts().head(top_n).reset_index()
        icd_counts.columns = ['icd_code', 'count']
        total_codes = self.df['icd_code'].count()
        icd_counts['percentage'] = (icd_counts['count'] / total_codes * 100).round(2)
        return icd_counts

# Example usage:
if __name__ == "__main__":
    analyzer = ICDAnalyzer("diagnoses_icd.csv")
    analyzer.run_analysis()
