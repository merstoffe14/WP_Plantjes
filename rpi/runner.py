import asyncio


class BackgroundRunner:
    def __init__(self):
        self.water_requested = False

    async def run_main(self):
        while True:
            await asyncio.sleep(1)
            self.loop()

    def loop(self):
        if self.water_requested:
            print("pumping water...")
            self.water_requested = False
