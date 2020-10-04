from read_file import read_file
from image_extracter import indi_image

import sys
import os
from PIL import Image


POSITIONS_FILE = "Positions - Performance.txt"


def main():
	scores = read_file(POSITIONS_FILE)
	input_path = sys.argv[1]
	if os.path.isfile(input_path):
		files = [input_path]
	else:
		files = [(input_path+"\\"+f) for f in os.listdir(input_path) if f.endswith(".jpg")]

	for file in files:
		with Image.open(file) as img:
			indi_image(img, scores)


if __name__ == "__main__":
	main()
