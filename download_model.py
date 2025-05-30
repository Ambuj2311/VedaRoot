import gdown
import os

def download_model():
    model_dir = "medicinal-plant-detection/backend/static/model"
    os.makedirs(model_dir, exist_ok=True)
    
    # Google Drive File ID (replace with your actual file ID)
    url = f"https://drive.google.com/file/d/19sx3tbj4yA_RR5p6by4OOm9LXR05XtAy/view?usp=sharing"
    
    output = f"{model_dir}/model.safetensors"
    gdown.download(url, output, quiet=False)
    print("Model downloaded successfully!")

if __name__ == "__main__":
    download_model()