"""Stream system metrics over WebSocket (demo mode prints a few samples)."""
import argparse
import asyncio
from pathlib import Path

try:
    import psutil
except Exception:
    psutil = None

try:
    import websockets
except Exception:
    websockets = None


async def demo_task():
    if psutil is None:
        print('Install requirements: psutil')
        return
    for i in range(3):
        print({'cpu_percent': psutil.cpu_percent(interval=0.1), 'mem_percent': psutil.virtual_memory().percent})
        await asyncio.sleep(0.5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    args = parser.parse_args()

    if args.demo:
        asyncio.run(demo_task())
        return

    if websockets is None or psutil is None:
        print('Install requirements: websockets psutil')
        return

    async def handler(ws, path):
        try:
            while True:
                data = {'cpu_percent': psutil.cpu_percent(interval=1), 'mem_percent': psutil.virtual_memory().percent}
                await ws.send(str(data))
        except Exception:
            pass

    print('Start metrics WebSocket server on ws://localhost:8767')
    start_server = websockets.serve(handler, 'localhost', 8767)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
