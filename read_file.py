import typing


class Position:
	x = 0
	y = 0

	def __init__(self, x=0, y=0):
		self.x = int(x)
		self.y = int(y)

	def __str__(self) -> str:
		return "(" + str(self.x) + ", " + str(self.y) + ")"


class Score:
	position_start = Position
	position_end = Position
	title = ""

	def __init__(self, position_start=Position, position_end=Position, title=""):
		self.position_start = position_start
		self.position_end = position_end
		self.title = title

	def __str__(self) -> str:
		return self.title + "\nStart: " + str(self.position_start) + "\nEnd: " + str(self.position_end) + "\n"


def read_file(filename: str) -> typing.List[Score]:
	scores = []
	with open(filename) as file:
		for line in file:
			if line != "":
				line = line.strip()
				line_values = line.split(';')
				pos_start = line_values[0].split(',')
				pos_end = line_values[1].split(',')
				title = line_values[2]
				score = Score(position_start=Position(pos_start[0], pos_start[1]),
								position_end=Position(pos_end[0], pos_end[1]),
								title=title)
				scores.append(score)

	return scores


def main():
	file = "Positions - Performance.txt"
	ratings = read_file(file)
	for rat in ratings:
		print(rat)


if __name__ == '__main__':
	main()
