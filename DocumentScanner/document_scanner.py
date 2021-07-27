import numpy as np
import cv2
import pygame
import os

def pre_processing(image, threshold1, threshold2):
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blur_image = cv2.GaussianBlur(gray_image, ksize=(5, 5), sigmaX=1)
	canny_image = cv2.Canny(blur_image, threshold1, threshold2)

	return canny_image

def get_contours(image):
	contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	biggest_contour = max(contours, key=cv2.contourArea)
	x, y, w, h = cv2.boundingRect(biggest_contour)

	return biggest_contour, x, y, w, h

def get_perspective(coordiantes, image, img_height, img_width):
	pts1 = np.float32(coordiantes)
	pts2 = np.float32([[0, 0], [img_width, 0], [0, img_height], [img_width, img_height]])

	matrix = cv2.getPerspectiveTransform(pts1, pts2)
	warp_image = cv2.warpPerspective(image, matrix, (img_width, img_height))

	return warp_image


def reading_image(path):
	org_img = cv2.imread(path)
	img_height, img_width = org_img.shape[:2]
	return org_img, img_height, img_width

def main(path, coordiantes):
	org_img, img_height, img_width = reading_image(path)

	median = np.median(org_img)
	threshold1 = int(max(0, (1-0.33)*median))
	threshold2 = int(min(255, (1+0.33)*median))

	image = pre_processing(org_img, 50, 150)

	biggest_contour, x, y, w, h = get_contours(image)

	warp_image = get_perspective(coordiantes, org_img, img_height, img_width)

	gray_image = cv2.cvtColor(warp_image, cv2.COLOR_BGR2GRAY)

	final_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 199, 5)

	cv2.imshow("Document", final_image)

	if cv2.waitKey(0) == ord('q'):
		cv2.destroyWindow("Document")
	if cv2.waitKey(0) == ord('s'):
		save_path = r"C:\Users\Pc\Desktop"
		cv2.imwrite(os.path.join(save_path , 'document.jpg'), final_image)

def get_coor(path):
	org_img, img_height, img_width = reading_image(path)
	coordiantes = []
	pygame.init()
	white = (255, 255, 255)
	display_surface = pygame.display.set_mode((img_width, img_height))
	pygame.display.set_caption('Image Coordinates')
	image = pygame.image.load(path)

	while True:
		display_surface.fill(white)
		display_surface.blit(image, (0, 0))

		events = pygame.event.get()
		for event in events:
			if event.type == pygame.MOUSEBUTTONUP:
				x, y = pygame.mouse.get_pos()
				coordiantes.append((x, y))
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					coordiantes = np.array(coordiantes)
					main(path, coordiantes)
					quit()


			pygame.display.update()






