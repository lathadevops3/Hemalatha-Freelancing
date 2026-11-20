"""Watch a directory for file changes and broadcast events over WebSocket (demo writes sample file changes)."""
import argparse
import asyncio
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except Exception:
    Observer = None
    FileSystemEventHandler = None

try:
    import websockets
except Exception:
    websockets = None

CONNECTED = set()


if FileSystemEventHandler is not None:
    class Handler(FileSystemEventHandler):
        def __init__(self, loop):
            self.loop = loop

        def on_created(self, event):
            msg = f'CREATED {event.src_path}'
            for ws in list(CONNECTED):
                try:
                    asyncio.run_coroutine_threadsafe(ws.send(msg), self.loop)
                except Exception:
                    pass
else:
    # Fallback handler when watchdog is not installed; provides compatible API
    class Handler:
        def __init__(self, loop):
            self.loop = loop

        def on_created(self, event):
            print(f'File created (watchdog not installed): {getattr(event, "src_path", event)}')


async def ws_handler(ws, path):
    CONNECTED.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        CONNECTED.remove(ws)


def demo_actions(folder: Path):
    folder.mkdir(exist_ok=True)
    for i in range(2):
        p = folder / f'demo_file_{i}.txt'
        p.write_text(f'demo {i}', encoding='utf-8')
    print('Wrote demo files')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--watch', default='watch_dir')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=8766)
    args = parser.parse_args()

    if Observer is None or websockets is None:
        print('Install requirements: watchdog websockets')
        return

    folder = Path(args.watch)

    if args.demo:
        demo_actions(folder)
        print("File watcher demo completed locally.")
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    event_handler = Handler(loop)
    observer = Observer()
    observer.schedule(event_handler, str(folder), recursive=False)
    observer.start()

    start_server = websockets.serve(ws_handler, args.host, args.port)
    loop.run_until_complete(start_server)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
