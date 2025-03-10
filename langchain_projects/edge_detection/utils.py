def get_image_gradient(image):
		image_gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
		image_gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
		return image_gradient_x, image_gradient_y
