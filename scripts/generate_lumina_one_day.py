import asyncio
import sys
from generate_lumina_days12_30 import DAYS, build_day

if __name__ == '__main__':
    day = int(sys.argv[1])
    if day not in DAYS:
        raise SystemExit(f'Unsupported day: {day}')
    asyncio.run(build_day(day, DAYS[day]))
