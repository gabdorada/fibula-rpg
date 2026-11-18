import sqlite3
from models import Player, Item 

class Database:
    def __init__(self, db_name='fibula_rpg.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Player Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                hp INTEGER,
                max_exp INTEGER,
                strength INTEGER,
                level INTEGER,
                exp INTEGER
            )
        """
        )
        # Player Inventory Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT,
                item_name TEXT,
                item_type TEXT,
                effect_value INTEGER,
                FOREIGN KEY(player_name) REFERENCES player(name)
            )
        """
        )
        self.conn.commit()

    def save_player(self, player: Player):
        cursor = self.conn.cursor()
        # Save or update player data
        cursor.execute(
            """
            INSERT OR REPLACE INTO player (name, hp, max_exp, strength, level, exp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, 
            (
                player.name,
                player.hp,
                player.max_exp,
                player.strength,
                player.level,
                player.exp,
            ),
        )

        # Clears old inventory from the database to rewrite it with updated data
        cursor.execute(
            "DELETE FROM inventory WHERE player_name = ?", (player.name,)
        )
        for item in player.inventory:
            cursor.execute(
                """ 
                INSERT INTO inventory (player_name, item_name, item_type, effect_value)
                VALUES (?, ?, ?, ?)
            """,
                (player.name, item.name, item.item_type, item.effect_value),
            )

        self.conn.commit()

    def load_player(self, name: str) -> Player | None:
        cursor = self.conn.cursor()
        cursor.execute (
            "SELECT name, hp, max_exp, strength, level, exp FROM player WHERE name = ?",
            (name,),
        )
        row = cursor.fetchone()

        if not row:
            return None

        # Load the inventory
        cursor.execute(
            "SELECT item_name, item_hype, effect_value FROM inventory WHERE player_name = ?",
            (name,),
        )
        item_rows = cursor.fetchall()
        inventory = [
            Item(name=r[0], item_type=r[1], effect_value=r[2])
            for r in item_rows
        ]

        # Returns the created Player instance
        return Player(
            name=row[0],
            hp=row[1],
            max_exp=row[2],
            strength=row[3],
            level=row[4],
            exp=row[5],
            inventory=inventory,
        )
    
    def close(self):
        self.conn.close()












# Teste rápido:
if __name__ == "__main__":
    db = Database()
    print("Banco de dados e tabelas criados com sucesso!")