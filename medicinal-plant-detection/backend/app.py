# ------------ backend/app.py ------------
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from PIL import Image
from transformers import ViTConfig, ViTForImageClassification, ViTImageProcessor
from safetensors.torch import load_file
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Required for server-side plotting

app = Flask(__name__)
CORS(app)

# Load model once at startup
def load_model():
    config = ViTConfig.from_pretrained("google/vit-base-patch16-224")
    config.num_labels = 52
    config.id2label = {str(i): label for i, label in enumerate([
        "Amla", "Curry", "Betel", "Bamboo", "Palak(Spinach)",
        "Coriender", "Ashoka", "Seethapala", "Lemon_grass", "Pappaya",
        "Curry_Leaf", "Lemon", "Nooni", "Henna", "Mango",
        "Doddpathre", "Amruta_Balli", "Betel_Nut", "Tulsi", "Pomegranate",
        "Castor", "Jackfruit", "Insulin", "Pepper", "Raktachandini",
        "Aloevera", "Jasmine", "Doddapatre", "Neem", "Geranium",
        "Rose", "Gauva", "Hibiscus", "Nithyapushpa", "Wood_sorel",
        "Tamarind", "Guava", "Bhrami", "Sapota", "Basale",
        "Avacado", "Ashwagandha", "Nagadali", "Arali", "Ekka",
        "Ganike", "Tulasi", "Honge", "Mint", "Catharanthus",
        "Papaya", "Brahmi"
    ])}
    
    model = ViTForImageClassification(config)
    model.load_state_dict(load_file("static/model/model.safetensors"))
    model.eval()
    processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
    return model, processor, config

model, processor, config = load_model()

plant_details = {
  "Amla": {
    "scientific_name": "Phyllanthus emblica",
    "common_uses": "Consumed as fruit, used in traditional medicine",
    "medicinal_uses": "Rich in vitamin C, boosts immunity, improves digestion, anti-aging properties"
  },
  "Curry": {
    "scientific_name": "Murraya koenigii",
    "common_uses": "Culinary herb, flavoring agent",
    "medicinal_uses": "Anti-diabetic, anti-inflammatory, helps digestion, prevents diarrhea"
  },
  "Betel": {
    "scientific_name": "Piper betle",
    "common_uses": "Stimulant, cultural significance",
    "medicinal_uses": "Relieves headaches, improves digestion, antiseptic properties"
  },
  "Bamboo": {
    "scientific_name": "Bambusoideae",
    "common_uses": "Construction, crafts, edible shoots",
    "medicinal_uses": "Anti-inflammatory, treats infections, promotes bone health"
  },
  "Palak(Spinach)": {
    "scientific_name": "Spinacia oleracea",
    "common_uses": "Leafy vegetable, culinary common_uses",
    "medicinal_uses": "Rich in iron, improves eyesight, boosts immunity"
  },
  "Coriender": {
    "scientific_name": "Coriandrum sativum",
    "common_uses": "Culinary herb, seasoning",
    "medicinal_uses": "Aids digestion, lowers blood sugar, rich in antioxidants"
  },
  "Ashoka": {
    "scientific_name": "Saraca asoca",
    "common_uses": "Ornamental plant, religious significance",
    "medicinal_uses": "Treats gynecological disorders, reduces inflammation, anti-bacterial"
  },
  "Seethapala": {
    "scientific_name": "Annona squamosa",
    "common_uses": "Edible fruit, traditional medicine",
    "medicinal_uses": "Anti-cancer properties, treats diarrhea, reduces swelling"
  },
  "Lemon_grass": {
    "scientific_name": "Cymbopogon citratus",
    "common_uses": "Culinary herb, tea ingredient",
    "medicinal_uses": "Reduces anxiety, lowers cholesterol, anti-inflammatory"
  },
  "Pappaya": {
    "scientific_name": "Carica papaya",
    "common_uses": "Edible fruit, meat tenderizer",
    "medicinal_uses": "Aids digestion, wound healing, boosts immunity"
  },
  "Curry_Leaf": {
    "scientific_name": "Murraya koenigii",
    "common_uses": "Culinary seasoning",
    "medicinal_uses": "Controls diabetes, improves eyesight, reduces stress"
  },
  "Lemon": {
    "scientific_name": "Citrus limon",
    "common_uses": "Culinary common_uses, cleaning agent",
    "medicinal_uses": "Rich in vitamin C, aids digestion, skin brightening"
  },
  "Nooni": {
    "scientific_name": "Morinda citrifolia",
    "common_uses": "Traditional medicine, juice",
    "medicinal_uses": "Boosts immunity, pain relief, anti-inflammatory"
  },
  "Henna": {
    "scientific_name": "Lawsonia inermis",
    "common_uses": "Hair dye, skin decoration",
    "medicinal_uses": "Cools body, treats skin disorders, anti-fungal"
  },
  "Mango": {
    "scientific_name": "Mangifera indica",
    "common_uses": "Edible fruit, culinary common_uses",
    "medicinal_uses": "Rich in vitamins, improves digestion, boosts immunity"
  },
  "Doddpathre": {
    "scientific_name": "Coleus aromaticus",
    "common_uses": "Culinary herb, flavoring",
    "medicinal_uses": "Treats cold, improves digestion, anti-bacterial"
  },
  "Amruta_Balli": {
    "scientific_name": "Tinospora cordifolia",
    "common_uses": "Traditional medicine",
    "medicinal_uses": "Boosts immunity, anti-diabetic, anti-inflammatory"
  },
  "Betel_Nut": {
    "scientific_name": "Areca catechu",
    "common_uses": "Stimulant, cultural common_uses",
    "medicinal_uses": "Aids digestion, vermifuge, mild stimulant"
  },
  "Tulsi": {
    "scientific_name": "Ocimum tenuiflorum",
    "common_uses": "Religious significance, herbal tea",
    "medicinal_uses": "Treats respiratory disorders, reduces stress, anti-bacterial"
  },
  "Pomegranate": {
    "scientific_name": "Punica granatum",
    "common_uses": "Edible fruit, juice",
    "medicinal_uses": "Rich in antioxidants, improves heart health, anti-inflammatory"
  },
  "Castor": {
    "scientific_name": "Ricinus communis",
    "common_uses": "Oil production, ornamental",
    "medicinal_uses": "Laxative, pain reliever, anti-inflammatory"
  },
  "Jackfruit": {
    "scientific_name": "Artocarpus heterophyllus",
    "common_uses": "Edible fruit, culinary common_uses",
    "medicinal_uses": "Boosts immunity, improves digestion, anti-cancer properties"
  },
  "Insulin": {
    "scientific_name": "Costus igneus",
    "common_uses": "Traditional medicine",
    "medicinal_uses": "Lowers blood sugar, anti-diabetic properties"
  },
  "Pepper": {
    "scientific_name": "Piper nigrum",
    "common_uses": "Spice, seasoning",
    "medicinal_uses": "Aids digestion, anti-inflammatory, rich in antioxidants"
  },
  "Raktachandini": {
    "scientific_name": "Pterocarpus santalinus",
    "common_uses": "Dye, traditional medicine",
    "medicinal_uses": "Cooling agent, treats skin disorders, anti-inflammatory"
  },
  "Aloevera": {
    "scientific_name": "Aloe barbadensis",
    "common_uses": "Cosmetics, skin care",
    "medicinal_uses": "Heals burns, improves digestion, skin hydration"
  },
  "Jasmine": {
    "scientific_name": "Jasminum officinale",
    "common_uses": "Perfume, ornamental",
    "medicinal_uses": "Reduces stress, antiseptic, improves mood"
  },
  "Doddapatre": {
    "scientific_name": "Coleus amboinicus",
    "common_uses": "Culinary herb, seasoning",
    "medicinal_uses": "Treats cold, cough, digestive aid"
  },
  "Neem": {
    "scientific_name": "Azadirachta indica",
    "common_uses": "Traditional medicine, pesticide",
    "medicinal_uses": "Anti-bacterial, blood purifier, treats skin disorders"
  },
  "Geranium": {
    "scientific_name": "Pelargonium graveolens",
    "common_uses": "Essential oil, ornamental",
    "medicinal_uses": "Anti-depressant, wound healing, balances hormones"
  },
  "Rose": {
    "scientific_name": "Rosa spp.",
    "common_uses": "Ornamental, perfumes",
    "medicinal_uses": "Cooling agent, improves mood, skin tonic"
  },
  "Gauva": {
    "scientific_name": "Psidium guajava",
    "common_uses": "Edible fruit, culinary",
    "medicinal_uses": "Rich in vitamin C, treats diarrhea, anti-diabetic"
  },
  "Hibiscus": {
    "scientific_name": "Hibiscus rosa-sinensis",
    "common_uses": "Ornamental, herbal tea",
    "medicinal_uses": "Lowers blood pressure, hair care, rich in antioxidants"
  },
  "Nithyapushpa": {
    "scientific_name": "Catharanthus roseus",
    "common_uses": "Ornamental, traditional medicine",
    "medicinal_uses": "Anti-cancer properties, treats diabetes, reduces blood pressure"
  },
  "Wood_sorel": {
    "scientific_name": "Oxalis acetosella",
    "common_uses": "Culinary herb, ornamental",
    "medicinal_uses": "Rich in vitamin C, diuretic, fever reducer"
  },
  "Tamarind": {
    "scientific_name": "Tamarindus indica",
    "common_uses": "Culinary, flavoring agent",
    "medicinal_uses": "Laxative, rich in antioxidants, improves digestion"
  },
  "Guava": {
    "scientific_name": "Psidium guajava",
    "common_uses": "Edible fruit, culinary",
    "medicinal_uses": "Rich in vitamin C, treats diarrhea, anti-diabetic"
  },
  "Bhrami": {
    "scientific_name": "Bacopa monnieri",
    "common_uses": "Traditional medicine",
    "medicinal_uses": "Brain tonic, reduces anxiety, improves memory"
  },
  "Sapota": {
    "scientific_name": "Manilkara zapota",
    "common_uses": "Edible fruit, culinary",
    "medicinal_uses": "Energy booster, improves digestion, anti-inflammatory"
  },
  "Basale": {
    "scientific_name": "Basella alba",
    "common_uses": "Leafy vegetable, culinary",
    "medicinal_uses": "Laxative, rich in iron, improves digestion"
  },
  "Avacado": {
    "scientific_name": "Persea americana",
    "common_uses": "Edible fruit, culinary",
    "medicinal_uses": "Heart healthy fats, skin nourishment, rich in vitamins"
  },
  "Ashwagandha": {
    "scientific_name": "Withania somnifera",
    "common_uses": "Traditional medicine",
    "medicinal_uses": "Reduces stress, boosts immunity, improves stamina"
  },
  "Nagadali": {
    "scientific_name": "Rauvolfia serpentina",
    "common_uses": "Traditional medicine",
    "medicinal_uses": "Treats hypertension, sedative, reduces anxiety"
  },
  "Arali": {
    "scientific_name": "Nerium oleander",
    "common_uses": "Ornamental, traditional medicine",
    "medicinal_uses": "Cardiac tonic (caution: toxic in large doses)"
  },
  "Ekka": {
    "scientific_name": "Calotropis gigantea",
    "common_uses": "Traditional medicine, fiber",
    "medicinal_uses": "Treats skin diseases, anti-inflammatory, pain reliever"
  },
  "Ganike": {
    "scientific_name": "Solanum nigrum",
    "common_uses": "Traditional medicine",
    "medicinal_uses": "Anti-inflammatory, treats liver disorders, fever reducer"
  },
  "Tulasi": {
    "scientific_name": "Ocimum tenuiflorum",
    "common_uses": "Religious, herbal tea",
    "medicinal_uses": "Respiratory health, reduces stress, anti-bacterial"
  },
  "Honge": {
    "scientific_name": "Pongamia pinnata",
    "common_uses": "Biofuel, traditional medicine",
    "medicinal_uses": "Anti-inflammatory, treats skin disorders, wound healing"
  },
  "Mint": {
    "scientific_name": "Mentha spp.",
    "common_uses": "Culinary, flavoring",
    "medicinal_uses": "Aids digestion, relieves nausea, respiratory health"
  },
  "Catharanthus": {
    "scientific_name": "Catharanthus roseus",
    "common_uses": "Ornamental, medicine",
    "medicinal_uses": "Anti-cancer properties, treats diabetes, reduces blood pressure"
  },
  "Papaya": {
    "scientific_name": "Carica papaya",
    "common_uses": "Edible fruit, culinary",
    "medicinal_uses": "Aids digestion, wound healing, boosts immunity"
  },
  "Brahmi": {
    "scientific_name": "Bacopa monnieri",
    "common_uses": "Traditional medicine",
    "medicinal_uses": "Brain tonic, improves memory, reduces anxiety"
  }
};


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Read image bytes
        img_bytes = file.read()
        
        # Convert to base64 for frontend display
        encoded_image = base64.b64encode(img_bytes).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{encoded_image}"
        
        # Process image
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model(**inputs)
            predicted_idx = outputs.logits.argmax(-1).item()
            confidence = torch.nn.functional.softmax(outputs.logits, dim=-1)[0][predicted_idx].item()
        
        prediction = {
            "class": config.id2label[str(predicted_idx)],
            "confidence": round(confidence * 100, 2),
            "details": plant_details.get(config.id2label[str(predicted_idx)], {}),
            "image": image_url  # Add image to response
        }

        return jsonify(prediction)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)