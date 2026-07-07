import os
import gdown

# Replace with your actual Google Drive File IDs
MODEL_FILE_ID = '1U4nSSK7laohKDhPVqG0wwb-jXlmMHETE'
ENV_FILE_ID = '1E9k38Tbb0Ss15VQ4bGWyjR-52QBfnCr7'

# Destinations inside the Docker container
MODEL_DEST = '/app/ml/embeddings/similarity.pkl'
ENV_DEST = '/app/backend/.env' 

if __name__ == "__main__":
    # 1. Download Model
    if not os.path.exists(MODEL_DEST):
        print(f"Downloading similarity.pkl to {MODEL_DEST}...")
        os.makedirs(os.path.dirname(MODEL_DEST), exist_ok=True)
        gdown.download(f'https://drive.google.com/uc?id={MODEL_FILE_ID}', MODEL_DEST, quiet=False)
        print("Model download complete!")
    else:
        print("similarity.pkl already exists. Skipping.")

    # 2. Download .env file
    # Set your desired destination

    ENV_DEST = '/app/backend/.env'

    

    # 2. Download .env file

    if not os.path.exists(ENV_DEST):

        print(f"Downloading .env to {ENV_DEST}...")

        

        # THE FIX: Tell Python to create the 'backend' folder if it's missing

        os.makedirs(os.path.dirname(ENV_DEST), exist_ok=True)

        

        gdown.download(f'https://drive.google.com/uc?id={ENV_FILE_ID}', ENV_DEST, quiet=False)

        print(".env download complete!")

    else:

        print(".env already exists. Skipping.")