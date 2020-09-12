from read_file import Position, Rating, read_file

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np


def main():
	positions_file = "ImagePositions.txt"
	image_file = "C:\\Users\\Joshua\\Documents\\Development\\FIFAStats\\Screenshots\\FIFA 20 Seasons (In Menus)_2.jpg"
	ratings = read_file(positions_file)
	extract_smaller_image(ratings[0].position_start, ratings[0].position_end, image_file)
	print("Hello World")


def extract_smaller_image(start_pos: Position, end_pos: Position, file: str):



if __name__ == "__main__":
	main()




im = np.array(Image.open('stinkbug.png'), dtype=np.uint8)

# Create figure and axes
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(im)

# Create a Rectangle patch
rect = patches.Rectangle((50,100),40,30,linewidth=1,edgecolor='r',facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect)

plt.show()