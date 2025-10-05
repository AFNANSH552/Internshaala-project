# Performance Analysis --Syeda shamama Afeef

## Project Overview

This project processes and visualizes performance data by analyzing Performance Ratio (PR) and Global Horizontal Irradiance (GHI) metrics over time. The system generates comprehensive visualizations showing performance trends, moving averages, and budget comparisons.

## Features

* **Data Processing** : Automatically combines PR and GHI data from multiple CSV files across different time periods
* **Performance Visualization** : Creates detailed graphs showing:
* Daily PR values color-coded by irradiation levels
* 30-day moving average trend line
* Dynamic budget line with yearly degradation (0.8% annual reduction)
* Statistical analysis (7d, 30d, 60d, 90d, 365d, and lifetime averages)
* **Date Range Filtering** : Supports custom date range analysis (bonus feature)
* **Automated Processing** : Single function to process all data files

## Dataset Structure

The project expects the following folder structure:

```
project/
├── PR/
│   ├── 2019-07/
│   │   ├── 2019-07-01.csv
│   │   ├── 2019-07-06.csv
│   │   └── ...
│   ├── 2019-08/
│   └── ...
├── GHI/
│   ├── 2019-07/
│   │   ├── 2019-07-01.csv
│   │   ├── 2019-07-06.csv
│   │   └── ...
│   ├── 2019-08/
│   └── ...
└── script.py
```

### Data Format

Each CSV file contains multiple days of data:

**PR CSV Format:**

```csv
Date,PR
2019-07-01,69.57567588
2019-07-02,79.31441128
```

**GHI CSV Format:**

```csv
Date,GHI
2019-07-01,3.256608333
2019-07-02,3.976766667
```

## Requirements

### Python Version

* Python 3.7 or higher

### Dependencies

Install required libraries:

```bash
pip install pandas numpy matplotlib seaborn
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

**requirements.txt:**

```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```
3. Place your PR and GHI data folders in the project directory
4. Run the script

## Usage

### Basic Usage

Process all data and generate visualization:

```bash
python script.py
```

This will:

1. Process all PR and GHI CSV files
2. Generate `processed_data.csv` with combined data
3. Create `pr_performance_graph.png` with the visualization

### Advanced Usage (Date Range Filtering)

To generate a graph for a specific date range, modify the `main()` function in `script.py`:

```python
def main():
    # Step 1: Preprocess data
    df = preprocess_data(pr_folder='PR', ghi_folder='GHI', 
                         output_csv='processed_data.csv')
  
    # Step 2: Generate graph for full dataset
    generate_graph(df, output_file='pr_performance_graph.png')
  
    # Step 3: Generate graph for specific date range
    generate_graph(df, 
                   start_date='2024-01-01', 
                   end_date='2024-06-30',
                   output_file='pr_performance_2024_h1.png')
```

### Function Reference

#### `preprocess_data(pr_folder, ghi_folder, output_csv)`

Processes all PR and GHI data files and combines them into a single CSV.

**Parameters:**

* `pr_folder` (str): Path to PR data folder (default: 'PR')
* `ghi_folder` (str): Path to GHI data folder (default: 'GHI')
* `output_csv` (str): Output CSV filename (default: 'processed_data.csv')

**Returns:**

* DataFrame with columns: Date, GHI, PR

#### `generate_graph(df, start_date, end_date, output_file)`

Generates performance visualization graph.

**Parameters:**

* `df` (DataFrame): Processed data with Date, GHI, PR columns
* `start_date` (str, optional): Start date for filtering (format: 'YYYY-MM-DD')
* `end_date` (str, optional): End date for filtering (format: 'YYYY-MM-DD')
* `output_file` (str): Output image filename (default: 'pr_performance_graph.png')

## Output Files

### 1. processed_data.csv

Combined dataset with three columns:

| Date       | GHI         | PR          |
| ---------- | ----------- | ----------- |
| 2019-07-01 | 3.256608333 | 69.57567588 |
| 2019-07-02 | 3.976766667 | 79.31441128 |
| ...        | ...         | ...         |

### 2. pr_performance_graph.png

Visualization showing:

* **Scatter Points** : Daily PR values color-coded by GHI intensity
* Navy blue: GHI < 2 kWh/m²
* Light blue: 2 ≤ GHI < 4 kWh/m²
* Orange: 4 ≤ GHI < 6 kWh/m²
* Brown: GHI ≥ 6 kWh/m²
* **Red Line** : 30-day moving average of PR
* **Green Line** : Dynamic budget line (starts at 73.9%, reduces 0.8% annually)
* **Statistics Box** : Average PR for multiple time periods
* **Performance Metrics** : Points above target budget

## Graph Components Explained

### Budget Line Calculation

The budget line represents the target performance ratio that degrades over time:

* **Initial Budget** : 73.9%
* **Annual Reduction** : 0.8%
* **Calculation** : Budget_PR = 73.9 × (1 - 0.008)^years_elapsed
* **Year Definition** : July to June (e.g., Year 1 = July 2019 to June 2020)

### GHI Color Coding

| GHI Range (kWh/m²) | Color      | Meaning                       |
| ------------------- | ---------- | ----------------------------- |
| < 2                 | Navy Blue  | Low irradiation (cloudy)      |
| 2-4                 | Light Blue | Moderate irradiation          |
| 4-6                 | Orange     | Good irradiation              |
| > 6                 | Brown      | Excellent irradiation (sunny) |

### Performance Metrics

* **Points above Target Budget PR** : Count and percentage of days where actual PR exceeded the budget line
* **Average PR Last 7d** : Rolling 7-day average
* **Average PR Last 30d** : Rolling 30-day average
* **Average PR Last 60d** : Rolling 60-day average
* **Average PR Last 90d** : Rolling 90-day average
* **Average PR Last 365d** : Rolling 365-day average
* **Average PR Lifetime** : Overall mean PR across all data

## Troubleshooting

### Issue: "Found 0 PR files"

 **Solution** : Check that:

* PR and GHI folders exist in the same directory as script.py
* Folder names are exactly "PR" and "GHI" (case-sensitive on some systems)
* CSV files exist inside the month subfolders

### Issue: "KeyError: 'Date'"

 **Solution** : Ensure CSV files have proper headers:

```csv
Date,PR
2019-07-01,69.57567588
```

### Issue: "No numeric types to aggregate"

 **Solution** : Check that PR and GHI values are numeric, not text. The script handles this automatically in the latest version.

### Issue: Getting fewer than expected rows

 **Solution** :

* Verify that all month folders contain CSV files
* Check that dates in PR and GHI files match
* Run with debug output to see which files are being processed

## Project Structure

```
project/
├── PR/                          # Performance Ratio data
│   └── YYYY-MM/                # Monthly folders
│       └── YYYY-MM-DD.csv      # Daily data files
├── GHI/                         # Global Horizontal Irradiance data
│   └── YYYY-MM/                # Monthly folders
│       └── YYYY-MM-DD.csv      # Daily data files
├── script.py                    # Main processing script
├── processed_data.csv           # Output: Combined dataset
├── pr_performance_graph.png     # Output: Visualization
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

## Technical Details

### Data Processing Logic

1. **File Discovery** : Recursively searches for all CSV files in PR and GHI folders
2. **Data Extraction** : Reads each CSV file and extracts all date-value pairs
3. **Data Merging** : Combines PR and GHI data by matching dates
4. **Data Validation** : Ensures numeric values and handles missing data
5. **Output Generation** : Creates sorted, clean CSV with Date, GHI, PR columns

### Visualization Logic

1. **Moving Average** : Calculates 30-day rolling mean of PR values
2. **Budget Calculation** : Dynamically computes target PR for each date
3. **Color Mapping** : Assigns colors based on GHI intensity ranges
4. **Statistical Analysis** : Computes averages for multiple time windows
5. **Graph Rendering** : Creates publication-quality visualization

## Performance Considerations

* **Processing Time** : ~2-5 seconds for ~1000 data points
* **Memory Usage** : ~50-100 MB for typical datasets
* **Output Size** :
* CSV: ~30-50 KB for 1000 rows
* PNG: ~200-500 KB at 300 DPI

## Future Enhancements

Potential improvements for future versions:

Interactive web dashboard

Real-time data processing

Additional performance metrics (availability, degradation rate)

Anomaly detection

Multi-plant comparison

Export to PDF reports

Command-line arguments for easier configuration

## License

This project is created for assessment purposes.

## Author

Created as part of a take-home assessment for performance analysis.

## Contact

For questions or issues, please refer to the project documentation or contact syedashamama459@gmail.com

---

Made by Syeda Shamama Afeef
