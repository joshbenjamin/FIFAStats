import sqlite3
from sqlite3 import Error
import typing


def create_connection(db_file: str) -> sqlite3.Connection:
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	"""
	finally:
		if conn:
			conn.close()
	"""
	return conn


def create_table(connection: sqlite3.Connection, create_table_sql: str):
	try:
		c = connection.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)


def create_game(connection: sqlite3.Connection, values: typing.Tuple[str]) -> sqlite3.Cursor:
	base_sql = '''
		INSERT INTO games (your_team, their_team, your_score, their_score, their_name, game_mode, game_date)
		VALUES(?, ?, ?, ?, ?, ?, ?)
	'''
	cursor = connection.cursor()
	cursor.execute(base_sql, values)
	connection.commit()
	return cursor.lastrowid


def process_game(dictionary: typing.Dict[str, str]) -> typing.Tuple[str]:
	tuple = ()

	for key in dictionary:
		if dictionary[key] == "":
			tuple = tuple + ("",)
		else:
			tuple = tuple + (dictionary[key],)

	return tuple


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
				their_team text NOT NULL,
				your_score integer NOT NULL,
				their_score integer NOT NULL,
				their_name text,
				game_mode text,
				game_date text
			);
	"""

	conn = create_connection(db_file)

	if conn:
		create_table(conn, create_table_game_sql)

		temp_game = {"your_team": "Chelsea", "their_team": "Barcelona", "your_score": "5", "their_score": "1",
					 "their_name": "", "game_mode": "", "game_date": ""}
		# game_tup = temp_game.values()
		game_tup = process_game(temp_game)
		create_game(conn, game_tup)

	else:
		print("No connection to the database")
