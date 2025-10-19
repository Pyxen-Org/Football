import asyncpg
import asyncio
from typing import Optional, List, Dict

# --------------------------
# DATABASE CONNECTION
# --------------------------
DATABASE_URL = "postgresql://postgres:****@shinkansen.proxy.rlwy.net:50906/railway"  # Replace with your DB URL

async def connect_db() -> asyncpg.Connection:
    """Connect to PostgreSQL using asyncpg"""
    conn = await asyncpg.connect(DATABASE_URL)
    return conn


# --------------------------
# TABLES
# --------------------------
# Tables assumed:
# 1. users(user_id BIGINT PRIMARY KEY, first_name TEXT, username TEXT)
# 2. games(game_id SERIAL PRIMARY KEY, chat_id BIGINT, host_id BIGINT REFERENCES users(user_id), status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT NOW())
# 3. players(player_id SERIAL PRIMARY KEY, game_id INT REFERENCES games(game_id), user_id BIGINT REFERENCES users(user_id), score INT DEFAULT 0)


# --------------------------
# USER FUNCTIONS
# --------------------------
async def add_user(conn: asyncpg.Connection, user_id: int, first_name: str, username: Optional[str]):
    """Add a user if not exists"""
    query = """
        INSERT INTO users (user_id, first_name, username)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id) DO NOTHING
    """
    await conn.execute(query, user_id, first_name, username)


async def get_user(conn: asyncpg.Connection, user_id: int) -> Optional[asyncpg.Record]:
    """Fetch a user by user_id"""
    query = "SELECT * FROM users WHERE user_id=$1"
    return await conn.fetchrow(query, user_id)


# --------------------------
# GAME FUNCTIONS
# --------------------------
async def create_game(conn: asyncpg.Connection, chat_id: int) -> int:
    """Create a new game in a chat, returns game_id"""
    query = "INSERT INTO games (chat_id) VALUES ($1) RETURNING game_id"
    row = await conn.fetchrow(query, chat_id)
    return row['game_id']


async def get_game(conn: asyncpg.Connection, chat_id: int) -> Optional[asyncpg.Record]:
    """Get the current pending game for a chat"""
    query = "SELECT * FROM games WHERE chat_id=$1 AND status='pending'"
    return await conn.fetchrow(query, chat_id)


async def set_host(conn: asyncpg.Connection, game_id: int, host_id: int):
    """Set the host of a game"""
    query = "UPDATE games SET host_id=$1 WHERE game_id=$2"
    await conn.execute(query, host_id, game_id)


async def end_game(conn: asyncpg.Connection, game_id: int):
    """Mark a game as completed"""
    query = "UPDATE games SET status='completed' WHERE game_id=$1"
    await conn.execute(query, game_id)


# --------------------------
# PLAYER FUNCTIONS
# --------------------------
async def add_player(conn: asyncpg.Connection, game_id: int, user_id: int):
    """Add a player to a game"""
    query = """
        INSERT INTO players (game_id, user_id)
        VALUES ($1, $2)
        ON CONFLICT (game_id, user_id) DO NOTHING
    """
    await conn.execute(query, game_id, user_id)


async def remove_player(conn: asyncpg.Connection, game_id: int, user_id: int):
    """Remove a player from a game"""
    query = "DELETE FROM players WHERE game_id=$1 AND user_id=$2"
    await conn.execute(query, game_id, user_id)


async def update_score(conn: asyncpg.Connection, game_id: int, user_id: int, score: int):
    """Update a player's score"""
    query = "UPDATE players SET score=$1 WHERE game_id=$2 AND user_id=$3"
    await conn.execute(query, score, game_id, user_id)


async def get_players(conn: asyncpg.Connection, game_id: int) -> List[asyncpg.Record]:
    """Get all players in a game"""
    query = "SELECT * FROM players WHERE game_id=$1"
    return await conn.fetch(query, game_id)


# --------------------------
# USAGE EXAMPLE (optional)
# --------------------------
# async def main():
#     conn = await connect_db()
#     await add_user(conn, 12345, "Shadow", "shad_bot")
#     game_id = await create_game(conn, -100123456789)
#     await set_host(conn, game_id, 12345)
#     await add_player(conn, game_id, 12345)
#     players = await get_players(conn, game_id)
#     print(players)
#     await conn.close()
#
# asyncio.run(main())
