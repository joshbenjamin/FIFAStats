import sqlite3
from sqlite3 import Error
import typing

ORDER_OF_GAME_KEYS = ["your_team", "their_team", "your_score", "their_score", "their_name", "game_mode", "game_date"]
ORDER_OF_GAME_DATA_KEYS = ["player_name", "match_rating_primary", "match_rating_secondary", "goals", "own_goals",
						   "goal_assists", "shots_on_target", "shots_total", "passes_completed", "passes_total",
						   "dribbles_completed", "dribbles_total", "crosses_completed", "crosses_total", "tackles_won",
						   "tackles_total", "saves"]


def create_connection(db_filename: str) -> sqlite3.Connection:
	connection = None
	try:
		connection = sqlite3.connect(db_filename)
		return connection
	except Error as e:
		print(e)
	return connection


def create_table(connection: sqlite3.Connection, create_table_sql: str):
	try:
		c = connection.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)


def create_game(connection: sqlite3.Connection, values: typing.Tuple[str]) -> int:
	base_sql = '''
		INSERT INTO games (your_team, their_team, your_score, their_score, their_name, game_mode, game_date)
		VALUES(?, ?, ?, ?, ?, ?, ?)
	'''
	cursor = connection.cursor()
	cursor.execute(base_sql, values)
	connection.commit()
	return cursor.lastrowid


def create_game_data(connection: sqlite3.Connection, values: typing.Tuple[str]):
	base_sql = '''
			INSERT INTO game_data (player_name, match_rating_primary, match_rating_secondary, goals, own_goals, 
			goal_assists, shots_on_target, shots_total, passes_completed, passes_total, dribbles_completed, 
			dribbles_total, crosses_completed, crosses_total, tackles_won, tackles_total, saves, game_id)
			VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	'''
	cursor = connection.cursor()
	cursor.execute(base_sql, values)
	connection.commit()


def process_data(dictionary: typing.Dict[str, str], is_game: bool) -> typing.Tuple[str]:
	temp_tuple = ()

	if is_game:
		for key in ORDER_OF_GAME_KEYS:
			if dictionary[key] == "":
				temp_tuple = temp_tuple + ("",)
			else:
				temp_tuple = temp_tuple + (str(dictionary[key]),)
	else:
		for key in ORDER_OF_GAME_DATA_KEYS:
			if dictionary[key] == "":
				temp_tuple = temp_tuple + ("",)
			else:
				temp_tuple = temp_tuple + (str(dictionary[key]),)

	return temp_tuple


if __name__ == "__main__":

	db_file = "fifa.db"

	create_table_game_sql = """
			CREATE TABLE IF NOT EXISTS games (
				id integer PRIMARY KEY,
				your_team text NOT NULL,
				their_team text NOT NULL,
				your_score integer NOT NULL,
				their_score integer NOT NULL,
				their_name text,
				game_mode text,
				game_date text
			);
	"""
	create_table_game_data_sql = """
			CREATE TABLE IF NOT EXISTS game_data (
				id integer PRIMARY KEY,
				player_name text NOT NULL,
				match_rating_primary integer NOT NULL,
				match_rating_secondary integer NOT NULL,
				goals integer NOT NULL,
				own_goals integer NOT NULL,
				goal_assists integer NOT NULL,
				shots_on_target integer NOT NULL,
				shots_total integer NOT NULL,
				passes_completed integer NOT NULL,
				passes_total integer NOT NULL,
				dribbles_completed integer NOT NULL,
				dribbles_total integer NOT NULL,
				crosses_completed integer NOT NULL,
				crosses_total integer NOT NULL,
				tackles_won integer NOT NULL,
				tackles_total integer NOT NULL,
				saves integer NOT NULL,
				game_id integer NOT NULL,
				FOREIGN KEY (game_id) REFERENCES games (id)
			);
	"""

	conn = create_connection(db_file)

	if conn:
		# create_table(conn, create_table_game_sql)
		create_table(conn, create_table_game_data_sql)

		temp_game = {
			"your_team": "Germany", "their_team": "Barcelona", "your_score": "4", "their_score": "3", "their_name": "",
			"game_mode": "Seasons", "game_date": "11/09/2020"
		}
		game_tup = process_data(temp_game, True)
		game_id = create_game(conn, game_tup)

		temp_game_data = {
			"player_name": "Kai Havertz", "match_rating_primary": 9, "match_rating_secondary": 3, "goals": 1,
			"own_goals": 0, "goal_assists": 1, "shots_on_target": 2, "shots_total": 6, "passes_completed": 26,
			"passes_total": 27, "dribbles_completed": 21, "dribbles_total": 22, "crosses_completed": 0,
			"crosses_total": 0, "tackles_won": 0, "tackles_total": 1, "saves": 0
		}
		game_data_tup = process_data(temp_game_data, False) + (str(game_id),)
		create_game_data(conn, game_data_tup)

	else:
		print("No connection to the database")
