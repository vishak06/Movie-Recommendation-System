"""
Complete Movie Dataset Processing Script
==========================================
This script performs two main operations:
1. Filters movies by region and popularity
2. Cleans the dataset by keeping only essential columns

Author: Cinema Project
Date: 2026-01-05
"""

import pandas as pd
import os
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

# Indian language codes
INDIAN_LANGUAGES = [
    'hi',  # Hindi
    'ta',  # Tamil
    'te',  # Telugu
    'ml',  # Malayalam
    'kn',  # Kannada
]

# Hollywood language
HOLLYWOOD_LANGUAGE = 'en'  # English

# Popularity thresholds for filtering
MIN_POPULARITY_INDIAN = 0.3    # Keep Indian movies with at least this popularity
MIN_POPULARITY_HOLLYWOOD = 2.0  # Keep top 10% of Hollywood movies
MIN_POPULARITY_OTHER = 5.0      # Keep only very popular movies from other countries
MIN_RUNTIME = 70                # Minimum runtime in minutes

# Columns to keep in final dataset
COLUMNS_TO_KEEP = [
    'title',
    'release_date',
    'original_language',
    'overview',
    'genres',
    'cast',
    'director',
    'imdb_rating',
    'poster_path'
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_language_name(code):
    """Get language name from code."""
    language_map = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'ml': 'Malayalam',
        'kn': 'Kannada',
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
        'ru': 'Russian',
    }
    return language_map.get(code, 'Unknown')

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

def print_subheader(text):
    """Print a formatted subheader."""
    print("\n" + "-" * 70)
    print(text)
    print("-" * 70)

# ============================================================================
# MAIN PROCESSING FUNCTION
# ============================================================================

def process_movies(
    input_file='TMDB_all_movies.csv',
    output_file='final_movies.csv',
    keep_intermediate=False
):
    """
    Complete movie dataset processing pipeline.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to the final output CSV file
        keep_intermediate (bool): Keep intermediate filtered file
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    print_header("MOVIE DATASET PROCESSING PIPELINE")
    print(f"\nInput file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"\nConfiguration:")
    print(f"  - Minimum popularity for Indian movies: {MIN_POPULARITY_INDIAN}") 
    print(f"  - Minimum popularity for Hollywood movies: {MIN_POPULARITY_HOLLYWOOD}")
    print(f"  - Minimum popularity for other movies: {MIN_POPULARITY_OTHER}")
    print(f"  - Minimum runtime: {MIN_RUNTIME} minutes")
    print(f"  - Columns to keep: {len(COLUMNS_TO_KEEP)}")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"\n[ERROR] Input file '{input_file}' not found!")
        return False
    
    file_size_mb = os.path.getsize(input_file) / (1024 * 1024)
    print(f"  - Input file size: {file_size_mb:.2f} MB")
    
    start_time = datetime.now()
    
    try:
        # ====================================================================
        # STEP 1: LOAD DATA
        # ====================================================================
        print_header("STEP 1: LOADING DATA")
        df = pd.read_csv(input_file, low_memory=False)
        print(f"[OK] Loaded {len(df):,} rows")
        print(f"[OK] Total columns: {len(df.columns)}")
        
        # Validate required columns
        if 'popularity' not in df.columns:
            print("[ERROR] 'popularity' column not found in the dataset!")
            return False
        
        if 'original_language' not in df.columns:
            print("[ERROR] 'original_language' column not found in the dataset!")
            return False

        # ====================================================================
        # STEP 1.5: FILTER BY RUNTIME
        # ====================================================================
        if 'runtime' in df.columns:
            print_header("STEP 1.5: FILTERING BY RUNTIME")
            before_runtime = len(df)
            df = df[df['runtime'] >= MIN_RUNTIME].copy()
            removed_runtime = before_runtime - len(df)
            print(f"[OK] Removed {removed_runtime:,} movies with runtime < {MIN_RUNTIME} mins")
            print(f"[OK] Remaining movies: {len(df):,}")
        else:
            print("\n[WARNING] 'runtime' column not found, skipping runtime filter")
        
        # ====================================================================
        # STEP 2: FILTER BY REGION AND POPULARITY
        # ====================================================================
        print_header("STEP 2: FILTERING BY REGION AND POPULARITY")
        
        # Fill NaN values in popularity with 0
        df['popularity'] = df['popularity'].fillna(0)
        
        print(f"\nOriginal dataset:")
        print(f"  - Total movies: {len(df):,}")
        print(f"  - Unique languages: {df['original_language'].nunique()}")
        
        # Create filtering conditions
        print("\nApplying filters...")
        
        # Condition 1: All Indian movies (no popularity filter)
        is_indian = df['original_language'].isin(INDIAN_LANGUAGES)
        is_indian_popular = is_indian & (df['popularity'] >= MIN_POPULARITY_INDIAN)
        indian_count = is_indian_popular.sum()
        print(f"  [OK] Indian movies (popularity >= {MIN_POPULARITY_INDIAN}): {indian_count:,}")
        
        # Condition 2: Popular Hollywood (English) movies
        is_hollywood = df['original_language'] == HOLLYWOOD_LANGUAGE
        is_hollywood_popular = is_hollywood & (df['popularity'] >= MIN_POPULARITY_HOLLYWOOD)
        hollywood_count = is_hollywood_popular.sum()
        print(f"  [OK] Hollywood movies (popularity >= {MIN_POPULARITY_HOLLYWOOD}): {hollywood_count:,}")
        
        # Condition 3: Very popular movies from other countries
        is_other_language = ~(is_indian | is_hollywood)
        is_other_popular = is_other_language & (df['popularity'] >= MIN_POPULARITY_OTHER)
        other_popular_count = is_other_popular.sum()
        print(f"  [OK] Other country movies (popularity >= {MIN_POPULARITY_OTHER}): {other_popular_count:,}")
        
        # Combine all conditions
        final_filter = is_indian_popular | is_hollywood_popular | is_other_popular
        
        # Apply filter
        df = df[final_filter].copy()
        
        print(f"\n[OK] Total movies after filtering: {len(df):,}")
        
        # ====================================================================
        # STEP 3: CLEAN COLUMNS
        # ====================================================================
        print_header("STEP 3: CLEANING COLUMNS")
        
        # Check which columns exist
        existing_columns = [col for col in COLUMNS_TO_KEEP if col in df.columns]
        missing_columns = [col for col in COLUMNS_TO_KEEP if col not in df.columns]
        
        if missing_columns:
            print("\n[WARNING] The following columns are not in the CSV:")
            for col in missing_columns:
                print(f"  - {col}")
        
        if not existing_columns:
            print("\n[ERROR] None of the specified columns exist in the CSV!")
            return False
        
        print(f"\n[OK] Keeping {len(existing_columns)} columns:")
        for col in existing_columns:
            print(f"  - {col}")
        
        # Select only the existing columns
        df = df[existing_columns].copy()
        
        # ====================================================================
        # STEP 4: REMOVE DUPLICATES
        # ====================================================================
        print_header("STEP 4: REMOVING DUPLICATES")
        
        before_dedup = len(df)
        df = df.drop_duplicates()
        duplicates_removed = before_dedup - len(df)
        
        if duplicates_removed > 0:
            print(f"[OK] Removed {duplicates_removed:,} duplicate rows")
        else:
            print(f"[OK] No duplicates found")
        
        print(f"[OK] Final row count: {len(df):,}")
        
        # ====================================================================
        # STEP 5: ADD PROPER INDEX NUMBERING
        # ====================================================================
        print_header("STEP 5: ADDING INDEX NUMBERING")
        
        # Reset index to start from 1
        df.reset_index(drop=True, inplace=True)
        df.index = df.index + 1
        df.index.name = 'index'
        
        print(f"[OK] Index numbered from 1 to {len(df):,}")
        
        # ====================================================================
        # STEP 6: SAVE FINAL DATASET
        # ====================================================================
        print_header("STEP 6: SAVING FINAL DATASET")
        
        print(f"\nSaving to '{output_file}'...")
        df.to_csv(output_file, index=True)
        
        output_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        
        # ====================================================================
        # FINAL RESULTS
        # ====================================================================
        print_header("PROCESSING COMPLETE")
        
        print(f"\n[FILE SIZES]")
        print(f"  Original: {file_size_mb:.2f} MB")
        print(f"  Final:    {output_size_mb:.2f} MB")
        print(f"  Reduction: {file_size_mb - output_size_mb:.2f} MB ({((file_size_mb - output_size_mb) / file_size_mb * 100):.1f}%)")
        
        print(f"\n[DATASET INFO]")
        print(f"  Total movies: {len(df):,}")
        print(f"  Columns: {len(df.columns)}")
        
        print(f"\n[BREAKDOWN]")
        print(f"  Indian movies: {indian_count:,} ({indian_count / len(df) * 100:.1f}%)")
        print(f"  Hollywood movies: {hollywood_count:,} ({hollywood_count / len(df) * 100:.1f}%)")
        print(f"  Other popular movies: {other_popular_count:,} ({other_popular_count / len(df) * 100:.1f}%)")
        
        print(f"\n[TOP 10 LANGUAGES]")
        lang_dist = df['original_language'].value_counts().head(10)
        for i, (lang, count) in enumerate(lang_dist.items(), 1):
            lang_name = get_language_name(lang)
            percentage = (count / len(df)) * 100
            print(f"  {i:2d}. {lang} ({lang_name:15s}): {count:7,} ({percentage:5.2f}%)")
        
        duration = (datetime.now() - start_time).total_seconds()
        print(f"\n[SUCCESS] Processing completed in {duration:.2f} seconds")
        print(f"[OUTPUT] {output_file}")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Display configuration
    print("\n" + "=" * 70)
    print("MOVIE DATASET PROCESSOR")
    print("=" * 70)
    print("\nThis script will:")
    print("  1. Filter movies by region and popularity")
    print("     - Keep ALL Indian movies")
    print(f"     - Keep Hollywood movies with popularity >= {MIN_POPULARITY_HOLLYWOOD}")
    print(f"     - Keep other country movies with popularity >= {MIN_POPULARITY_OTHER}")
    print("  2. Clean dataset by keeping only essential columns")
    print("  3. Remove duplicate entries")
    print("  3. Remove duplicate entries")
    
    # Run the processing
    success = process_movies(
        input_file='TMDB_all_movies.csv',
        output_file='final_movies.csv',
        keep_intermediate=False
    )
    
    if success:
        print("\n[INFO] You can now use 'final_movies.csv' for your recommendation system!")
        print("\n[INFO] To adjust settings, edit the configuration section at the top of this script.")
    else:
        print("\n[ERROR] Processing failed. Please check the error messages above.")
