import aiohttp
import asyncio
from typing import Optional
from .exceptions import BotrixException

class Bot:
    def __init__(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)

class BotrixClient:
    def __init__(self, *, loop=None):
        self.loop = loop if loop is not None else asyncio.get_running_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.post_count = 0
        self.post_last = 0

    async def __aenter__(self):
        if not self.session:
            self.session = aiohttp.ClientSession(loop=self.loop)
        return self

    async def __aexit__(self, *err):
        if not self.session.closed:
            await asyncio.sleep(0)
            await self.session.close()
        self.session = None
    
    async def get_bot(self, _id) -> Optional[Bot]:
        ''' Returns information of the specified bot '''
        async with self.session.get(f'https://botrix.cc/api/v1/bot/{_id}') as resp:
            data = await resp.json()
        bot = data.get('bot')
        if bot == 'bot id not found':
            return None
        return Bot(bot)

    async def check_vote(self, bot_id, user_id) -> bool:
        ''' Checks if `user_id` has voted for `bot_id` and returns a corresponding boolean value '''
        async with self.session.get(f'https://botrix.cc/api/v1/voted/{bot_id}/{user_id}') as resp:
            data = await resp.json()
        if 'ERROR' in data:
            raise BotrixException(data.get('ERROR'))
        return data.get('voted')

    async def post_bot_data(self, _id, **kwargs):
        async with self.session.post('') as resp:
            pass

    async def close(self) -> None:
        ''' Closes the session. It is recommended you use the async context manager instead. '''
        if self.session:
            await asyncio.sleep(0)
            await self.session.close()

    

