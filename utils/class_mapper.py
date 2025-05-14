def map_to_three_classes(predicted_class):
    if predicted_class == "Organic":
        return "organik"

    elif predicted_class in [
        "Battery", "Electronic waste", "Lightbulb", "Paint can", "Medical waste", "Chemical container", "B3"
    ]:
        return "b3"

    else:
        return "anorganik"
