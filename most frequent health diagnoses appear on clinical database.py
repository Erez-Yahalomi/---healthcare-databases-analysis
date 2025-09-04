import pandas as pd
from typing import Optional


class ICDAnalyzer:
    """
    Analyzes ICD codes from a diagnoses CSV file and computes the top N codes/ diseases
    appear on patients diagnosis, along with their percentage of total diagnoses and descriptions.

    requirements: csv files of, d_icd_diagnoses.csv and d_icd_diagnoses.csv. 
    A link to demo of these files can be found in README. 
         
    """
    
    def __init__(self, diagnoses_path: str, dictionary_path: Optional[str] = None, top_n: int = 10) -> None:
        
        
        self.diagnoses_path =  "enter path to diagnoses_path.csv"
        self.dictionary_path = "enter path to d_icd_diagnoses.csv" 
        self.top_n = top_n

    def load_diagnoses(self) -> pd.DataFrame:
        """Loads and cleans the diagnoses data."""
        df = pd.read_csv(self.diagnoses_path, usecols=["icd_code", "icd_version"])
        df["icd_code"] = df["icd_code"].astype(str).str.strip()
        df["icd_version"] = pd.to_numeric(df["icd_version"], errors="coerce").astype("Int64")
        df = df.dropna(subset=["icd_code", "icd_version"])
        return df

    def load_dictionary(self) -> Optional[pd.DataFrame]:
        """Loads ICD dictionary with long titles if available."""
        if not self.dictionary_path:
            return None
        try:
            df = pd.read_csv(self.dictionary_path, usecols=["icd_code", "icd_version", "long_title"])
            df["icd_code"] = df["icd_code"].astype(str).str.strip()
            df["long_title"] = df["long_title"].astype(str).str.strip()
            df["icd_version"] = pd.to_numeric(df["icd_version"], errors="coerce").astype("Int64")
            df = df.dropna(subset=["icd_code", "icd_version"])
            return df.drop_duplicates(subset=["icd_code", "icd_version"])
        except Exception as e:
            print(f"[WARN] Could not load dictionary: {e}")
            return None

    def compute_top_icd(self, df: pd.DataFrame) -> pd.DataFrame:
        """Computes top N ICD codes and their percentage of total."""
        total = len(df)
        grouped = (
            df.groupby(["icd_code", "icd_version"])
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
            .head(self.top_n)
        )
        grouped["percent"] = (grouped["count"] / total).round(4)
        return grouped.reset_index(drop=True)

    def enrich_with_descriptions(self, top_df: pd.DataFrame, dict_df: Optional[pd.DataFrame]) -> pd.DataFrame:
        """Adds long_title descriptions to the top ICD codes."""
        if dict_df is None:
            top_df["long_title"] = None
            return top_df
        merged = top_df.merge(dict_df, on=["icd_code", "icd_version"], how="left")
        return merged[["icd_code", "icd_version", "long_title", "count", "percent"]]

    def run(self) -> pd.DataFrame:
        """Runs the full analysis pipeline."""
        diagnoses_df = self.load_diagnoses()
        dictionary_df = self.load_dictionary()
        top_icd_df = self.compute_top_icd(diagnoses_df)
        final_df = self.enrich_with_descriptions(top_icd_df, dictionary_df)
        return final_df


# Example usage:
if __name__ == "__main__":
    analyzer = ICDAnalyzer("diagnoses_icd.csv", "d_icd_diagnoses.csv", top_n=10)
    result = analyzer.run()
    print(result.to_string(index=False))
