import os
import gdown

# Replace with your actual Google Drive File IDs
MODEL_FILE_ID = '1U4nSSK7laohKDhPVqG0wwb-jXlmMHETE'

# Destinations inside the Docker container
MODEL_DEST = '/app/ml/embeddings/similarity.pkl'

if __name__ == "__main__":
    # 1. Download Model
    if not os.path.exists(MODEL_DEST):
        print(f"Downloading similarity.pkl to {MODEL_DEST}...")
        os.makedirs(os.path.dirname(MODEL_DEST), exist_ok=True)
        gdown.download(f'https://drive.google.com/uc?id={MODEL_FILE_ID}', MODEL_DEST, quiet=False)
        print("Model download complete!")
    else:
        print("similarity.pkl already exists. Skipping.")