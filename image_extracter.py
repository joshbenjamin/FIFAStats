from read_file import Position, Score, read_file
from tesseract_functions import *

from PIL import Image
import math
import cv2
import pytesseract
import typing

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

START_POSITION_MAIN = Position(613, 204)
END_POSITION_MAIN = Position(1702, 808)


def main():
	positions_file = "Positions - Performance.txt"
	image_file = "C:\\Users\\Joshua\\Documents\\Development\\FIFAStats\\Screenshots\\FIFA 20 Seasons (In Menus)_6.jpg"

	image = Image.open(image_file)
	scores = read_file(positions_file)

	crop_ratings_image(image)


def tesseract_work(filename: str):
	image = cv2.imread(filename)
	gray = get_grayscale(image)
	thresh = thresholding(gray)

	h, w, c = thresh.shape
	boxes = pytesseract.image_to_boxes(thresh)
	for b in boxes.splitlines():
		b = b.split(' ')
		thresh = cv2.rectangle(thresh, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

	cv2.imshow('img', thresh)
	cv2.waitKey(0)

	custom_config = r'--oem 3 --psm 6'
	print(pytesseract.image_to_string(thresh, config=custom_config))
	# cv2.imshow('thresh', thresh)
	# cv2.waitKey(0)


def crop_ratings_image(image: Image):
	width_height = width_and_height(START_POSITION_MAIN, END_POSITION_MAIN)
	im_crop = image.crop((START_POSITION_MAIN.x,
						  START_POSITION_MAIN.y,
						  START_POSITION_MAIN.x + width_height[0],
						  START_POSITION_MAIN.y + width_height[1]))
	im_crop.save("temp.png", "PNG")
	tesseract_work("temp.png")


def rating_type(image: Image, scores: typing.List[Score]) -> str:

	for score in scores:
		width_height = width_and_height(score.position_start, score.position_end)
		im_crop = image.crop((score.position_start.x,
							  score.position_start.y,
							  score.position_start.x + width_height[0],
							  score.position_start.y + width_height[1]))

	return ""


def analyse_block(image: Image) -> bool:
	count = 0
	colours = {'R': 0, 'G': 0, 'B': 0}
	for x in range(0, int(image.width/3)):
		for y in range(0, int(image.height/3)):
			count += 1
			colour_tup = image.getpixel((x, y))
			colours['R'] += colour_tup[0]
			colours['G'] += colour_tup[1]
			colours['B'] += colour_tup[2]

	for key in colours:
		colours[key] /= count

	# @Todo need a MUCH better classifier than this
	if colours['G'] < 100 or colours['B'] < 100:
		return True
	else:
		return False


def width_and_height(start_pos: Position, end_pos: Position) -> typing.Tuple[int, int]:
	abs_x = int(math.fabs(end_pos.x - start_pos.x))
	abs_y = int(math.fabs(end_pos.y - start_pos.y))
	return abs_x, abs_y


if __name__ == "__main__":
	main()
