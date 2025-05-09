def map_to_six_classes(predicted_class):
    if predicted_class == "Organic":
        return "organik"
    elif predicted_class in ["Paper", "Paper bag", "Paper cups", "Paper shavings", "Papier mache", "Cardboard", "Cellulose", "Printing industry"]:
        return "kertas"
    elif predicted_class in [
        "Plastic bag", "Plastic bottle", "Plastic can", "Plastic canister", "Plastic caps", "Plastic cup", "Plastic shaker",
        "Plastic shavings", "Plastic toys", "Combined plastic", "Zip plastic bag", "Stretch film", "Tetra pack",
        "Unknown plastic", "Ramen Cup", "Food Packet"
    ]:
        return "plastik"
    elif predicted_class in ["Glass bottle", "Ceramic"]:
        return "kaca"
    elif predicted_class in [
        "Aluminum can", "Aluminum caps", "Iron utensils", "Metal shavings", "Scrap metal", "Tin", "Foil"
    ]:
        return "logam"
    else:
        return "lainnya"
