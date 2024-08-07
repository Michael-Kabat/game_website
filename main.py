import asyncio
from Game import Game

game = Game()

async def main():
    game.play()

asyncio.run(main())