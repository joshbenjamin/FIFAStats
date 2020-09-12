from read_file import Position, Rating, read_file

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import math

import typing

from random import randint, seed


def main():
	seed(1)
	positions_file = "ImagePositions.txt"
	image_file = "C:\\Users\\Joshua\\Documents\\Development\\FIFAStats\\Screenshots\\FIFA 20 Seasons (In Menus)_2.jpg"
	ratings = read_file(positions_file)
	extract_smaller_image(ratings[0].position_start, ratings[0].position_end, image_file, ratings)
	print("Hello World")


def extract_smaller_image(start_pos: Position, end_pos: Position, file: str, ratings):

	colours = {0: 'r', 1: 'g', 2: 'b'}

	im = np.array(Image.open(file), dtype=np.uint8)

	# Create figure and axes
	fig, ax = plt.subplots(1)

	# Display the image
	ax.imshow(im)
	colour_int = 0

	for rat in ratings:
		# Create a Rectangle patch
		colour_int = (colour_int + 1) % 3
		width_height = width_and_height(rat.position_start, rat.position_end)
		rect = patches.Rectangle((rat.position_start.x, rat.position_start.y), width_height[0], width_height[1],
								 linewidth=1, edgecolor=colours[colour_int], facecolor='none')

		# Add the patch to the Axes
		ax.add_patch(rect)

	plt.show()


def width_and_height(start_pos: Position, end_pos: Position) -> typing.Tuple[int, int]:
	abs_x = int(math.fabs(end_pos.x - start_pos.x))
	abs_y = int(math.fabs(end_pos.y - end_pos.x))
	return (abs_x, abs_y)


if __name__ == "__main__":
	main()
