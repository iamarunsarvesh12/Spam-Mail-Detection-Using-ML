import pandas as pd
import os

# Paths for your files (Update these if your files are in a different folder)
ORIGINAL_TSV_PATH = 'data/spam_dataset.tsv'
ENRON_CSV_PATH = 'enron_spam_data.csv'  # Extracted from your zip file
OUTPUT_TSV_PATH = 'data/improved_spam_dataset.tsv'

def merge_and_clean():
    print("Loading original dataset...")
    # Assuming original dataset doesn't have headers, so we name them 'label' and 'message'
    df_original = pd.read_csv(ORIGINAL_TSV_PATH, sep='\t', names=['label', 'message'])
    
    print("Loading Enron dataset...")
    try:
        # Enron dataset loading
        df_enron = pd.read_csv(ENRON_CSV_PATH)
        
        # Enron dataset usually has columns like 'Spam/Ham' and 'Message'
        # Let's filter only the required columns and rename them to match our TSV
        df_enron = df_enron[['Spam/Ham', 'Message']].copy()
        df_enron.columns = ['label', 'message']
        
        # Convert labels if they are different (e.g., 'spam'/'ham')
        df_enron['label'] = df_enron['label'].str.lower()
        
    except KeyError:
        print("Error: Column names in Enron CSV didn't match. Please check the CSV headers.")
        return

    print("Merging datasets...")
    # Combine both datasets into one
    df_merged = pd.concat([df_original, df_enron], ignore_index=True)

    print("Cleaning data...")
    # Remove any empty rows
    df_merged.dropna(subset=['label', 'message'], inplace=True)
    
    # Remove exact duplicate messages to prevent model overfitting
    df_merged.drop_duplicates(subset=['message'], inplace=True)

    # Shuffle the data completely so spam and ham are mixed well
    df_merged = df_merged.sample(frac=1, random_state=42).reset_index(drop=True)

    print(f"Saving new dataset to {OUTPUT_TSV_PATH}...")
    # Save the new dataset in the same TSV format (Tab separated, no headers)
    df_merged.to_csv(OUTPUT_TSV_PATH, sep='\t', index=False, header=False)
    
    print("Done! 🎉")
    print(f"Total messages in original: {len(df_original)}")
    print(f"Total messages in Enron: {len(df_enron)}")
    print(f"Total messages in NEW dataset (after removing duplicates): {len(df_merged)}")

if __name__ == "__main__":
    merge_and_clean()