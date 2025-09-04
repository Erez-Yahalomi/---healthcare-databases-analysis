import pandas as pd

class PatientDataAnalyzer:
    """
    A class to encapsulate analysis methods for patient data from the MIMIC dataset.
     
    Use the format of MIMIC, patients.csv database file. Link to demo database files in this format is in README.
   
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the analyzer by reading the dataset.
        
        Parameters
        ----------
        file_path : str
            Path to the CSV file containing patient data.
        """
        self.df = pd.read_csv(file_path)
    
    def gender_distribution(self) -> pd.Series:
        """
        Calculate the gender distribution of patients in the dataset.
        
        Returns
        -------
        pd.Series
            A series where the index is gender categories and the values 
            are counts of patients in each category.
        """
        # Ensure gender column exists
        if 'gender' not in self.df.columns:
            raise ValueError("The dataset does not contain a 'gender' column.")
        
        # Count occurrences of each gender
        distribution = self.df['gender'].value_counts()
    
        return distribution


# --- Running the code on the attached dataset ---

# Path to the attached dataset
file_path = "write full path here"

# Create analyzer instance
analyzer = PatientDataAnalyzer(file_path)

# Get gender distribution
gender_dist = analyzer.gender_distribution()

print(gender_dist)
