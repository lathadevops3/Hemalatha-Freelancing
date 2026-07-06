"""Simple WebSocket chat server with a demo mode that broadcasts messages."""
import argparse
import asyncio
from typing import Set

try:
    import websockets
except Exception:
    websockets = None

CONNECTED: Set = set()


async def handler(ws, path):
    CONNECTED.add(ws)
    try:
        async for msg in ws:
            # broadcast
            for c in CONNECTED:
                if c is not ws:
                    await c.send(msg)
    finally:
        CONNECTED.remove(ws)


async def demo_task():
    print("Demo: starting WebSocket chat server for 3 seconds (no external clients)")
    await asyncio.sleep(0.1)
    print("Demo complete.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    if websockets is None:
        print("Please install requirements: websockets")
        return

    if args.demo:
        asyncio.run(demo_task())
        return

    print(f"WebSocket chat server listening on ws://{args.host}:{args.port}")
    start_server = websockets.serve(handler, args.host, args.port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
