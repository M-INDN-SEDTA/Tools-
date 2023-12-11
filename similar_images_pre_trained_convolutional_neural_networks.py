#Make sure to replace the placeholder paths with the actual paths to your images
import numpy as np
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity

def load_and_preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def get_image_features(model, img_array):
    features = model.predict(img_array)
    features = features.flatten()  # Flatten to create a 1D feature vector
    return features

def find_similar_images(query_image_path, image_paths, top_n=5):
    model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    query_img_array = load_and_preprocess_image(query_image_path)
    query_features = get_image_features(model, query_img_array)

    similar_images = []

    for path in image_paths:
        img_array = load_and_preprocess_image(path)
        features = get_image_features(model, img_array)

        # Calculate cosine similarity
        similarity = cosine_similarity([query_features], [features])[0][0]

        similar_images.append((path, similarity))

    # Sort by similarity (higher is more similar)
    similar_images.sort(key=lambda x: x[1], reverse=True)

    # Return top N similar images
    return similar_images[:top_n]

if __name__ == "__main__":
    query_image_path = "path/to/query/image.jpg"
    image_paths = ["path/to/image1.jpg", "path/to/image2.jpg", "path/to/image3.jpg", ...]

    similar_images = find_similar_images(query_image_path, image_paths)

    print(f"Similar images to {query_image_path}:")
    for i, (path, similarity) in enumerate(similar_images, 1):
        print(f"{i}. Image: {path}, Similarity: {similarity:.4f}")
