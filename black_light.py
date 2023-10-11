import cv2
import numpy as np

def adjust_image_for_uv_light(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Could not read the image.")
        return

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to improve visibility
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Enhance colors (optional)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * 1.5, 0, 255)  # Increase saturation
    enhanced_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return enhanced_image, binary_image

# Example usage:
input_image_path = 'RG001.jpeg'
processed_image, binary_image = adjust_image_for_uv_light(input_image_path)

# Display the processed image
cv2.imshow("Processed Image", processed_image)
cv2.imshow("Binary Image", binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
