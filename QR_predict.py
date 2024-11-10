import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import keras


def plot_image(img_path):
    """Load and display the image."""
    img = Image.open(img_path)
    img = img.convert("RGB")
    plt.imshow(img)
    plt.axis("off")  # Hide axes
    plt.show()


def predict(img_path, net):
    """Load the image, preprocess it, and predict."""
    img = Image.open(img_path)
    img = img.convert("RGB")  # Ensure image is in RGB mode
    img = img.resize((50, 50))

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Check the shape of the image array
    print(f"Image array shape: {img_array.shape}")

    propability = net.predict(img_array)
    prediction = (propability > 0.5).astype("int32")

    return "Malware" if prediction[0] == 1 else "Benign", (
        propability[0][0] if prediction[0] == 1 else 1 - propability[0][0]
    )


###### Example ######
# Load model
net = keras.models.load_model(r"assets/net1.keras")

# Path to image
img_path = "test/ben_C.png"

# Plot the image
plot_image(img_path)

# Make prediction
prediction, propability = predict(img_path=img_path, net=net)
print(f"{prediction} with probability {(propability * 100):0.2f}%")
