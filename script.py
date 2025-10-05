import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime, timedelta
import os

def preprocess_data(pr_folder='PR', ghi_folder='GHI', output_csv='processed_data.csv'):
    """
    Process PR and GHI data from folder structure and combine into single CSV.
    
    Args:
        pr_folder: Path to PR data folder
        ghi_folder: Path to GHI data folder
        output_csv: Output CSV filename
    
    Returns:
        DataFrame with columns: Date, GHI, PR
    """
    print("Starting data preprocessing...")
    
    # Initialize dictionary to store data by date
    data_dict = {}
    
    # Process PR files
    pr_path = Path(pr_folder)
    pr_files = sorted(pr_path.rglob('*.csv'))
    
    print(f"Found {len(pr_files)} PR files")
    
    # Read all PR data
    for pr_file in pr_files:
        try:
            pr_df = pd.read_csv(pr_file)
            # Each file has Date and PR columns
            for _, row in pr_df.iterrows():
                date = row['Date']
                pr_value = row['PR']
                if date not in data_dict:
                    data_dict[date] = {'Date': date, 'PR': None, 'GHI': None}
                data_dict[date]['PR'] = pr_value
        except Exception as e:
            print(f"Error processing {pr_file}: {e}")
    
    print(f"Loaded PR data for {len(data_dict)} dates")
    
    # Process GHI files
    ghi_path = Path(ghi_folder)
    ghi_files = sorted(ghi_path.rglob('*.csv'))
    
    print(f"Found {len(ghi_files)} GHI files")
    
    # Read all GHI data
    for ghi_file in ghi_files:
        try:
            ghi_df = pd.read_csv(ghi_file)
            # Each file has Date and GHI columns
            for _, row in ghi_df.iterrows():
                date = row['Date']
                ghi_value = row['GHI']
                if date not in data_dict:
                    data_dict[date] = {'Date': date, 'PR': None, 'GHI': None}
                data_dict[date]['GHI'] = ghi_value
        except Exception as e:
            print(f"Error processing {ghi_file}: {e}")
    
    # Convert dictionary to DataFrame
    df = pd.DataFrame(list(data_dict.values()))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Select only the required columns in the correct order
    df = df[['Date', 'GHI', 'PR']]
    
    # Debug info
    print(f"\nData statistics:")
    print(f"  Dates with PR data: {df['PR'].notna().sum()}")
    print(f"  Dates with GHI data: {df['GHI'].notna().sum()}")
    print(f"  Dates with both PR and GHI: {(df['PR'].notna() & df['GHI'].notna()).sum()}")
    print(f"  Missing PR values: {df['PR'].isna().sum()}")
    print(f"  Missing GHI values: {df['GHI'].isna().sum()}")
    
    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"\nData preprocessing complete!")
    print(f"Total rows: {len(df)}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Output saved to: {output_csv}")
    
    return df


def generate_graph(df, start_date=None, end_date=None, output_file='pr_performance_graph.png'):
    """
    Generate PR performance visualization with moving averages and budget line.
    
    Args:
        df: DataFrame with Date, GHI, PR columns
        start_date: Start date for filtering (format: 'YYYY-MM-DD')
        end_date: End date for filtering (format: 'YYYY-MM-DD')
        output_file: Output image filename
    """
    print("\nGenerating visualization...")
    
    # Filter data by date range if provided
    df_plot = df.copy()
    if start_date:
        df_plot = df_plot[df_plot['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df_plot = df_plot[df_plot['Date'] <= pd.to_datetime(end_date)]
    
    print(f"Plotting {len(df_plot)} data points")
    
    # Calculate 30-day moving average
    df_plot['PR_MA_30'] = df_plot['PR'].rolling(window=30, min_periods=1).mean()
    
    # Define color mapping for GHI values
    def get_ghi_color(ghi):
        if pd.isna(ghi):
            return '#808080'  # Gray for missing data
        elif ghi < 2:
            return '#00008B'  # Dark blue (Navy)
        elif 2 <= ghi < 4:
            return '#4169E1'  # Royal blue (< 2)
        elif 4 <= ghi < 6:
            return '#FFA500'  # Orange (2~4)
        else:
            return '#8B4513'  # Brown (> 6)
    
    df_plot['color'] = df_plot['GHI'].apply(get_ghi_color)
    
    # Calculate dynamic budget line
    # Budget starts at 73.9 and reduces by 0.8% every year
    # Year starts from July (month 7)
    first_date = df_plot['Date'].min()
    last_date = df_plot['Date'].max()
    
    # Determine the first July reference point
    if first_date.month >= 7:
        ref_year = first_date.year
    else:
        ref_year = first_date.year - 1
    
    budget_start_date = pd.Timestamp(f'{ref_year}-07-01')
    
    def calculate_budget_pr(date):
        """Calculate budget PR for a given date"""
        years_elapsed = (date - budget_start_date).days / 365.25
        initial_budget = 73.9
        annual_reduction = 0.008  # 0.8%
        budget_pr = initial_budget * ((1 - annual_reduction) ** years_elapsed)
        return budget_pr
    
    df_plot['Budget_PR'] = df_plot['Date'].apply(calculate_budget_pr)
    
    # Calculate points above budget
    df_plot['Above_Budget'] = (df_plot['PR'] > df_plot['Budget_PR']).astype(int)
    points_above_budget = df_plot['Above_Budget'].sum()
    total_points = len(df_plot)
    percentage_above = (points_above_budget / total_points * 100) if total_points > 0 else 0
    
    # Calculate average PR for different periods
    last_7_avg = df_plot['PR'].tail(7).mean()
    last_30_avg = df_plot['PR'].tail(30).mean()
    last_60_avg = df_plot['PR'].tail(60).mean()
    last_90_avg = df_plot['PR'].tail(90).mean()
    last_365_avg = df_plot['PR'].tail(365).mean()
    lifetime_avg = df_plot['PR'].mean()
    
    # Calculate budget PR values for each year
    years = []
    year_start = budget_start_date
    while year_start <= last_date:
        year_end = year_start + pd.DateOffset(years=1) - pd.DateOffset(days=1)
        budget_value = calculate_budget_pr(year_start)
        years.append(f"1Y~{budget_value:.1f}%")
        year_start = year_start + pd.DateOffset(years=1)
    
    budget_label = f"Target Budget Yield Performance Ratio [{','.join(years)}]"
    
    # Create figure with white background
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
    ax.set_facecolor('white')
    
    # Plot scatter points (PR values colored by GHI)
    scatter = ax.scatter(df_plot['Date'], df_plot['PR'], 
                        c=df_plot['color'], s=25, alpha=0.7, zorder=3, edgecolors='none')
    
    # Plot 30-day moving average (red line)
    ax.plot(df_plot['Date'], df_plot['PR_MA_30'], 
            color='#FF4444', linewidth=2.5, label='30~d moving average of PR', zorder=4)
    
    # Plot budget line (dark green)
    ax.plot(df_plot['Date'], df_plot['Budget_PR'], 
            color='#2D5016', linewidth=2.5, label=budget_label, zorder=2)
    
    # Formatting
    ax.set_xlabel('', fontsize=11)
    ax.set_ylabel('Performance Ratio [%]', fontsize=11)
    
    # Title with date range
    title = f"Performance Ratio Evolution\nFrom {first_date.strftime('%Y~%m~%d')} to {last_date.strftime('%Y~%m~%d')}"
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='gray')
    ax.set_ylim(0, 105)
    
    # Format x-axis to show dates nicely
    import matplotlib.dates as mdates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center')
    
    # Create custom legend for GHI colors at the top
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#00008B', label='< 2', edgecolor='none'),
        Patch(facecolor='#4169E1', label='2~4', edgecolor='none'),
        Patch(facecolor='#FFA500', label='4~6', edgecolor='none'),
        Patch(facecolor='#8B4513', label='> 6', edgecolor='none')
    ]
    
    legend1 = ax.legend(handles=legend_elements, loc='upper center', 
                       title='Daily Irradiation [kWh/m2]', framealpha=1,
                       ncol=4, bbox_to_anchor=(0.5, 1.0), fontsize=9,
                       title_fontsize=9, columnspacing=1)
    ax.add_artist(legend1)
    
    # Add line legends
    ax.legend(loc='upper left', framealpha=1, fontsize=8)
    
    # Add statistics text on the graph
    stats_y_pos = 35
    stats_text = f"Points above Target Budget PR = {points_above_budget}/{total_points} = {percentage_above:.1f}%"
    ax.text(0.5, stats_y_pos, stats_text, transform=ax.get_yaxis_transform(),
            fontsize=9, ha='center', 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='gray', linewidth=1))
    
    # Add text box with averages on the right side
    stats_lines = [
        f"Average PR last 7~d: {last_7_avg:.1f} %",
        f"Average PR last 30~d: {last_30_avg:.1f} %",
        f"Average PR last 60~d: {last_60_avg:.1f} %",
        f"Average PR last 90~d: {last_90_avg:.1f} %",
        f"Average PR last 365~d: {last_365_avg:.1f} %",
        f"Average PR Lifetime: {lifetime_avg:.1f} %"
    ]
    
    stats_text_box = '\n'.join(stats_lines)
    
    # Position text box on the right side
    props = dict(boxstyle='round', facecolor='white', alpha=1, edgecolor='black', linewidth=1)
    ax.text(1.02, 0.5, stats_text_box, transform=ax.transAxes, 
            fontsize=9, verticalalignment='center', horizontalalignment='left',
            bbox=props, family='monospace')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Graph saved to: {output_file}")
    plt.show()


def main():
    """Main function to run the complete workflow"""
    # Step 1: Preprocess data
    df = preprocess_data(pr_folder='PR', ghi_folder='GHI', 
                         output_csv='processed_data.csv')
    
    # Step 2: Generate graph
    generate_graph(df, output_file='pr_performance_graph.png')
    
    # Bonus: Generate graph for specific date range
    # Uncomment the lines below to test date filtering
    # generate_graph(df, start_date='2024-01-01', end_date='2024-06-30',
    #                output_file='pr_performance_graph_2024_h1.png')


if __name__ == "__main__":
    main()