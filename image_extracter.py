from read_file import Position, Rating, read_file

from PIL import Image
import math

import typing

START_POSITION_MAIN = Position(613, 204)
END_POSITION_MAIN = Position(1702, 808)


def main():
	positions_file = "ImagePositions.txt"
	image_file = "C:\\Users\\Joshua\\Documents\\Development\\FIFAStats\\Screenshots\\FIFA 20 Seasons (In Menus)_6.jpg"
	image = Image.open(image_file)
	ratings = read_file(positions_file)
	print("Rating: " + rating_type(image, ratings))
	crop_ratings_image(image)


def crop_ratings_image(image: Image):
	width_height = width_and_height(START_POSITION_MAIN, END_POSITION_MAIN)
	im_crop = image.crop((START_POSITION_MAIN.x,
						  START_POSITION_MAIN.y,
						  START_POSITION_MAIN.x + width_height[0],
						  START_POSITION_MAIN.y + width_height[1]))
	im_crop.show()


def rating_type(image: Image, ratings: typing.List[Rating]) -> str:

	for rat in ratings:
		width_height = width_and_height(rat.position_start, rat.position_end)
		im_crop = image.crop((rat.position_start.x,
						   rat.position_start.y,
						   rat.position_start.x + width_height[0],
						   rat.position_start.y + width_height[1]))

		if analyse_block(im_crop):
			print("THIS IS THE ONE: " + rat.title)
			# im_crop.show()
			return rat.title

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
