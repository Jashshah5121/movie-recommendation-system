import os
import gdown

# Replace with your actual Google Drive File ID
FILE_ID = '1U4nSSK7laohKDhPVqG0wwb-jXlmMHETE'

# Make sure this path matches where your backend expects the file to be!
DESTINATION = '/app/ml/embeddings/similarity.pkl' 

if __name__ == "__main__":
    if not os.path.exists(DESTINATION):
        print(f"Downloading similarity.pkl to {DESTINATION}...")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(DESTINATION), exist_ok=True)
        
        url = f'https://drive.google.com/uc?id={FILE_ID}'
        gdown.download(url, DESTINATION, quiet=False)
        print("Download complete!")
    else:
        print("similarity.pkl already exists. Skipping download.")