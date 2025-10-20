import asyncpg
import asyncio

# =========================
# DATABASE CONFIGURATION
# =========================
DATABASE_URL = "postgresql://postgres:NEqIXtgwKZQoBWFIqfbasqJQzkCMWDpY@postgres.railway.internal:5432/railway"

# =========================
# CONNECTION FUNCTION
# =========================
async def connect_db():
    return await asyncpg.connect(DATABASE_URL)

# =========================
# GAME CREATION
# =========================
async def create_game(chat_id: int, host_id: int, host_name: str):
    conn = await connect_db()
    try:
        await conn.execute("""
            INSERT INTO games (chat_id, host_id, host_name, status)
            VALUES ($1, $2, $3, 'waiting')
            ON CONFLICT (chat_id) DO UPDATE
            SET host_id = EXCLUDED.host_id,
                host_name = EXCLUDED.host_name,
                status = 'waiting';
        """, chat_id, host_id, host_name)
    finally:
        await conn.close()

# =========================
# FETCH GAME DATA
# =========================
async def get_game(chat_id: int):
    conn = await connect_db()
    try:
        return await conn.fetchrow("SELECT * FROM games WHERE chat_id = $1;", chat_id)
    finally:
        await conn.close()

# =========================
# SET HOST
# =========================
async def set_host(chat_id: int, host_id: int, host_name: str):
    conn = await connect_db()
    try:
        await conn.execute("""
            UPDATE games
            SET host_id = $1, host_name = $2
            WHERE chat_id = $3;
        """, host_id, host_name, chat_id)
    finally:
        await conn.close()

# =========================
# SIMPLE TEST (RUN DIRECTLY)
# =========================
if __name__ == "__main__":
    async def test():
        await create_game(123456, 78910, "Shadow")
        game = await get_game(123456)
        print(game)

    asyncio.run(test())
