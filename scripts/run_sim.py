from __future__ import annotations
import sys
import asyncio


def main() -> None:
    sys.path.insert(0, 'src')
    sys.path.insert(0, 'scripts')
    from simulate_send import main as run
    asyncio.run(run())


if __name__ == '__main__':
    main()

