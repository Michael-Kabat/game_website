import asyncio
import pygame
from Game import Game

game = Game()

async def main():
    await game.play()

asyncio.run(main())