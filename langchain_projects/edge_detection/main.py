import cv2
import numpy as np
def edge_detection(image):
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		image = cv2.GaussianBlur(image, (5, 5), 0)
		image = cv2.Canny(image, 100, 200)
		return image
if __name__ == "__main__":
		image = cv2.imread("image.jpg")
		edge_detected_image = edge_detection(image)
		cv2.imshow("Edge Detected Image", edge_detected_image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
