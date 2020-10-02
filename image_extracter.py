from read_file import Position, Score, read_file
from tesseract_functions import *

from PIL import Image
import numpy
import math
import cv2
import pytesseract
import typing

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

START_POSITION_MAIN = Position(613, 204)
END_POSITION_MAIN = Position(1702, 808)


def main():
	positions_file = "Positions - Performance.txt"
	image_filepath = "C:\\Users\\Joshua\\Documents\\Development\\FIFAStats\\Pictures - Performance\\Mason.jpg"

	image = Image.open(image_filepath)
	scores = read_file(positions_file)

	indi_image(image, scores)


def indi_image(image: Image, scores: typing.List[Score]):
	# for score in scores:

	# for i in range(0, len(scores)):
	for i in range(5, 6):
		score = scores[i]
		width_height = width_and_height(score.position_start, score.position_end)
		im_crop = image.crop((score.position_start.x,
							  score.position_start.y,
							  score.position_start.x + width_height[0],
							  score.position_start.y + width_height[1]))
		# im_crop.show(score.title, im_crop)
		# im_crop.save("temp.png", "PNG")
		analyse_image("number", im_crop)


def analyse_image(type_char: str, image: Image):
	cv2_image = numpy.array(image.convert('RGB'))
	# cv2_image = cv2_image[:, :, ::-1].copy()           unused, to convert RGB-to-BGR
	if type_char == "number":
		tesseract_work(cv2_image)


def tesseract_work(image: numpy.ndarray):
	# image = cv2.imread(filename)
	# gray = get_grayscale(image)
	# thresh = thresholding(image)

	""" This is to draw rectangles """
	"""
	h, w, c = thresh.shape
	boxes = pytesseract.image_to_boxes(thresh)
	for b in boxes.splitlines():
		b = b.split(' ')
		thresh = cv2.rectangle(thresh, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
	"""

	# Show image
	# cv2.imshow('img', image)
	# cv2.waitKey(0)

	custom_config = r'--oem 3 --psm 6'
	image_text = pytesseract.image_to_string(image, config=custom_config)
	image_text = strip_arrow(image_text)


def strip_arrow(text: str):
	text = text.replace(chr(12), '').strip()
	return text


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
