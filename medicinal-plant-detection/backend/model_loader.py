import numpy as np
from PIL import Image
import torch
from safetensors import safe_open
from safetensors.torch import save_model

#First download the model model.safetensors from my google drive link: https://drive.google.com/file/d/19sx3tbj4yA_RR5p6by4OOm9LXR05XtAy/view?usp=sharing 
#put the model in the folder medicinal-plant-detection > backend > static > model, then proceed further otherwise this app won't work.


class PlantDetectionModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.labels = [
  "Amla",
  "Curry",
  "Betel",
  "Bamboo",
  "Palak(Spinach)",
  "Coriender",
  "Ashoka",
  "Seethapala",
  "Lemon_grass",
  "Pappaya",
  "Curry_Leaf",
  "Lemon",
  "Nooni",
  "Henna",
  "Mango",
  "Doddpathre",
  "Amruta_Balli",
  "Betel_Nut",
  "Tulsi",
  "Pomegranate",
  "Castor",
  "Jackfruit",
  "Insulin",
  "Pepper",
  "Raktachandini",
  "Aloevera",
  "Jasmine",
  "Doddapatre",
  "Neem",
  "Geranium",
  "Rose",
  "Gauva",
  "Hibiscus",
  "Nithyapushpa",
  "Wood_sorel",
  "Tamarind",
  "Guava",
  "Bhrami",
  "Sapota",
  "Basale",
  "Avacado",
  "Ashwagandha",
  "Nagadali",
  "Arali",
  "Ekka",
  "Ganike",
  "Tulasi",
  "Honge",
  "Mint",
  "Catharanthus",
  "Papaya",
  "Brahmi"
]
        
    def load_model(self):
        """Load the safetensors model"""
        self.model = torch.jit.load(self.model_path)
        self.model.eval()
        
    def preprocess_image(self, image_path):
        """Preprocess the image for model input"""
        img = Image.open(image_path)
        img = img.resize((224, 224))  # Adjust based on your model's expected input
        img_array = np.array(img) / 255.0
        img_tensor = torch.FloatTensor(img_array).permute(2, 0, 1).unsqueeze(0)
        return img_tensor
    
    def predict(self, image_path):
        """Make a prediction on the input image"""
        if self.model is None:
            self.load_model()
            
        input_tensor = self.preprocess_image(image_path)
        with torch.no_grad():
            outputs = self.model(input_tensor)
        
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        top_prob, top_catid = torch.topk(probabilities, 1)
        
        return {
            'class': self.labels[top_catid.item()],
            'confidence': top_prob.item()
        }