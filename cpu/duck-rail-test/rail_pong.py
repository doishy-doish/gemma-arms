import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from duckapi_duckai import DuckAISession
async def main():
    s = DuckAISession(model="tinfoil/gemma4-31b", timeout=240.0)
    try:
        reply = await s.send("reply with exactly this word and nothing else: PONG", rewrite={"model": "tinfoil/gemma4-31b"})
        print("REPLY-OK len=", len(reply))
        print("REPLY-HEAD:", reply[:300])
    finally:
        await s.close()
asyncio.run(main())
