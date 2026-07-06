"""Log tailer that serves a tiny web UI and pushes appended log lines over WebSocket."""
import argparse
import asyncio
from pathlib import Path

try:
    from aiohttp import web, WSMsgType
except Exception:
    web = None


async def tail_file(path: Path, app):
    # simple polling tail
    pos = 0
    while True:
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if len(text) > pos:
                chunk = text[pos:]
                pos = len(text)
                for ws in app['sockets']:
                    await ws.send_str(chunk)
        await asyncio.sleep(0.5)


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app['sockets'].append(ws)
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT and msg.data == 'close':
                await ws.close()
    finally:
        request.app['sockets'].remove(ws)
    return ws


async def demo(app):
    sample = app['log_path']
    sample.write_text('2026-07-06 12:00:00 INFO Demo log line\n', encoding='utf-8')
    await asyncio.sleep(0.5)
    sample.write_text(sample.read_text(encoding='utf-8') + '2026-07-06 12:00:01 ERROR Demo error\n', encoding='utf-8')
    await asyncio.sleep(0.5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()

    if web is None:
        print('Please install requirements: aiohttp')
        return

    app = web.Application()
    app['sockets'] = []
    app['log_path'] = Path(__file__).parent / 'application.log'
    app.router.add_get('/ws', websocket_handler)

    loop = asyncio.get_event_loop()
    loop.create_task(tail_file(app['log_path'], app))
    if args.demo:
        loop.create_task(demo(app))

    web.run_app(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
