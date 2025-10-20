
import asyncpg
import asyncio

# =========================
# DATABASE CONFIGURATION
# =========================
DATABASE_URL = "postgresql://postgres:NEqIXtgwKZQoBWFIqfbasqJQzkCMWDpY@shinkansen.proxy.rlwy.net:50906/railway"

# =========================
# CONNECTION POOL
# =========================
_pool: asyncpg.pool.Pool = None

async def init_db():
    """Initialize connection pool and create tables if not exist."""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
    
    async with _pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS games (
                game_id SERIAL PRIMARY KEY,
                chat_id BIGINT NOT NULL UNIQUE,
                host_id BIGINT NOT NULL,
                host_name TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'waiting',
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

# =========================
# GAME CREATION
# =========================
async def create_game(chat_id: int, host_id: int, host_name: str):
    async with _pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO games (chat_id, host_id, host_name, status)
            VALUES ($1, $2, $3, 'waiting')
            ON CONFLICT (chat_id) DO UPDATE
            SET host_id = EXCLUDED.host_id,
                host_name = EXCLUDED.host_name,
                status = 'waiting';
        """, chat_id, host_id, host_name)

# =========================
# FETCH GAME DATA
# =========================
async def get_game(chat_id: int):
    async with _pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM games WHERE chat_id = $1;", chat_id)

# =========================
# SET HOST
# =========================
async def set_host(chat_id: int, host_id: int, host_name: str):
    async with _pool.acquire() as conn:
        await conn.execute("""
            UPDATE games
            SET host_id = $1, host_name = $2
            WHERE chat_id = $3;
        """, host_id, host_name, chat_id)

# =========================
# SIMPLE TEST (RUN DIRECTLY)
# =========================
if __name__ == "__main__":
    async def test():
        await init_db()  # ensure table exists
        await create_game(123456, 78910, "Shadow")
        game = await get_game(123456)
        print(game)

    asyncio.run(test())
