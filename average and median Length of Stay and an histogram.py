import pandas as pd

class AdmissionsAnalyzer:
    """
    A class to analyze hospital admissions data, specifically focusing
    on Length of Stay (LOS) calculations.
    """

    def __init__(self, file_path: str):
        """
        Initialize the analyzer by reading the admissions dataset.

        Parameters
        ----------
        file_path : str
            Path to the CSV file containing admissions data.
            Use the format of MIMIC, admissions.csv database file. Link to demo database files in this format is in README 
        """
        file_path = "write full path to admissions.csv database file here"


        # Load dataset into a DataFrame
        self.df = pd.read_csv(file_path)

        # Convert datetime columns to pandas datetime objects for calculations
        if "admittime" in self.df.columns and "dischtime" in self.df.columns:
            self.df["admittime"] = pd.to_datetime(self.df["admittime"])
            self.df["dischtime"] = pd.to_datetime(self.df["dischtime"])
        else:
            raise ValueError("Dataset must contain 'admittime' and 'dischtime' columns.")

    def calculate_length_of_stay(self) -> pd.Series:
        """
        Compute the Length of Stay (LOS) in days for each admission.

        Returns
        -------
        pd.Series
            A Series of LOS values in days (float), excluding invalid values.
        """
        # Calculate LOS in days: (discharge time - admit time)
        los = (self.df["dischtime"] - self.df["admittime"]).dt.total_seconds() / (24 * 3600)

        # Filter out invalid stays: negative or zero LOS
        los_clean = los[los > 0]

        return los_clean

    def average_and_median_los(self) -> dict:
        """
        Calculate the average and median Length of Stay across all admissions,
        using only valid LOS values.

        Returns
        -------
        dict
            A dictionary with keys 'average' and 'median' (in days).
        """
        los = self.calculate_length_of_stay()

        return {
            "average": los.mean(),
            "median": los.median(),
            "count_used": len(los)  # number of valid admissions included
        }

# ---------------------- print results----------------------
 

if __name__ == "__main__":
    # path to admissions.csv file
    file_path = "write full path here"

    # Create an analyzer object
    analyzer = AdmissionsAnalyzer(file_path)

    # Compute average and median LOS
    los_stats = analyzer.average_and_median_los()

    print("📊 Length of Stay Statistics (valid records only):")
    print(f"Average Length of Stay  (days): {los_stats['average']:.2f}")
    print(f"Median Length of Stay  (days): {los_stats['median']:.2f}")
    print(f"Valid admissions included: {los_stats['count_used']}")


 def plot_los_histogram(self, bins=None):
        """
        Plot a histogram of Length of Stay values.

        Parameters
        ----------
        bins : list, optional
            Custom bin edges for the histogram.
        """
        los = self.calculate_length_of_stay()

        if bins is None:
            bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

        plt.figure(figsize=(8, 5))
        plt.hist(los, bins=bins, edgecolor="black", alpha=0.7)
        plt.title("Histogram of Length of Stay (Days)")
        plt.xlabel("Length of Stay (days)")
        plt.ylabel("Number of Admissions")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    # Plot histogram with custom bins
    analyzer.plot_los_histogram(bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])