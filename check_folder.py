import os
from pathlib import Path

def check_folder_structure():
    """
    Check and display the current folder structure to help debug.
    """
    print("=" * 60)
    print("FOLDER STRUCTURE CHECKER")
    print("=" * 60)
    
    current_dir = Path.cwd()
    print(f"\nCurrent working directory: {current_dir}\n")
    
    # List all items in current directory
    print("Contents of current directory:")
    print("-" * 60)
    items = list(current_dir.iterdir())
    if items:
        for item in sorted(items):
            if item.is_dir():
                print(f"📁 {item.name}/")
            else:
                print(f"📄 {item.name}")
    else:
        print("Directory is empty!")
    
    print("\n" + "=" * 60)
    
    # Check for PR folder
    pr_folder = current_dir / 'PR'
    print("\nChecking PR folder:")
    print("-" * 60)
    if pr_folder.exists():
        print(f"✅ PR folder found at: {pr_folder}")
        
        # List subdirectories in PR
        pr_subdirs = [d for d in pr_folder.iterdir() if d.is_dir()]
        print(f"\nSubdirectories in PR: {len(pr_subdirs)}")
        for subdir in sorted(pr_subdirs)[:5]:  # Show first 5
            print(f"  📁 {subdir.name}/")
            # Show first few CSV files in each subdir
            csv_files = list(subdir.glob('*.csv'))
            for csv in csv_files[:3]:
                print(f"     📄 {csv.name}")
        
        # Count total PR CSV files
        pr_files = list(pr_folder.rglob('*_PR.csv'))
        print(f"\nTotal PR CSV files found: {len(pr_files)}")
        if pr_files:
            print("\nFirst 5 PR files:")
            for f in pr_files[:5]:
                print(f"  {f.relative_to(current_dir)}")
    else:
        print(f"❌ PR folder NOT found at: {pr_folder}")
    
    print("\n" + "=" * 60)
    
    # Check for GHI folder
    ghi_folder = current_dir / 'GHI'
    print("\nChecking GHI folder:")
    print("-" * 60)
    if ghi_folder.exists():
        print(f"✅ GHI folder found at: {ghi_folder}")
        
        # Count total GHI CSV files
        ghi_files = list(ghi_folder.rglob('*_GHI.csv'))
        print(f"\nTotal GHI CSV files found: {len(ghi_files)}")
        if ghi_files:
            print("\nFirst 5 GHI files:")
            for f in ghi_files[:5]:
                print(f"  {f.relative_to(current_dir)}")
    else:
        print(f"❌ GHI folder NOT found at: {ghi_folder}")
    
    print("\n" + "=" * 60)
    print("\nDIAGNOSTICS:")
    print("-" * 60)
    
    # Check if data might be in a different location
    print("\nSearching for any CSV files in current directory tree...")
    all_csvs = list(current_dir.rglob('*.csv'))
    print(f"Total CSV files found: {len(all_csvs)}")
    
    if all_csvs:
        print("\nFirst 10 CSV files found:")
        for csv in all_csvs[:10]:
            print(f"  {csv.relative_to(current_dir)}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    check_folder_structure()