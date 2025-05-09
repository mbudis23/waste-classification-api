import torch
import torch.nn as nn
from efficientnet_pytorch import EfficientNet

num_classes = 44
class_names = [
    "Aerosols",
"Aluminum can",
"Aluminum caps",
"Cardboard",
"Cellulose",
"Ceramic",
"Combined plastic",
"Container for household chemicals",
"Disposable tableware",
"Electronics",
"Foil",
"Furniture",
"Glass bottle",
"Iron utensils",
"Liquid",
"Metal shavings",
"Milk bottle",
"Organic",
"Paper bag",
"Paper cups",
"Paper shavings",
"Paper",
"Papier mache",
"Plastic bag",
"Plastic bottle",
"Plastic can",
"Plastic canister",
"Plastic caps",
"Plastic cup",
"Plastic shaker",
"Plastic shavings",
"Plastic toys",
"Postal packaging",
"Printing industry",
"Scrap metal",
"Stretch film",
"Tetra pack",
"Textile",
"Tin",
"Unknown plastic",
"Wood",
"Zip plastic bag", 
"Ramen Cup",
"Food Packet"
]

model_eff = EfficientNet.from_name('efficientnet-b0')
model_eff._fc = nn.Linear(model_eff._fc.in_features, num_classes)
model_eff.load_state_dict(torch.load("models/weight/efficientnet_garbage_classifier.pth", map_location="cpu"))
model_eff.eval()
