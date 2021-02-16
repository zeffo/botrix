import aiohttp
import asyncio
from typing import Optional
from .exceptions import BotrixException, RatelimitException

class Bot:
    __slots__ = [
    'botTags', 
    'certified', 
    'votes', 
    'usersVoted', 
    'state', 
    'owners', 
    'servers', 
    'shards', 
    'users', 
    'views', 
    'nsfw', 
    'bannerURL', 
    'webhook', 
    'inRecomendationQueue', 
    'badges', 
    '_id', 
    'botid', 
    'prefix', 
    'description', 
    'logo', 
    'username', 
    'botLibrary', 
    'invite', 
    'long', 
    'website', 
    'support', 
    'addedAt', 
    '_data'
    ]

    def __init__(self, data):
        self._data = data.get('bot')
        for key in self.__slots__:
            if key in self._data:
                setattr(self, key, self._data[key])

    def __bool__(self):
        if self._data == 'bot id not found':
            return None
        return True 


class BotrixClient:
    ''' Client interface which interacts with the Botrix API. It is recommended you use this as an Async Context Manager. '''
    def __init__(self, *, loop=None, debug=False) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self.debug = debug
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.BASE_URL = 'https://botrix.cc/api/v1'
    
    async def __aenter__(self):
        if not self.session:
            self.session = aiohttp.ClientSession(loop=self.loop)
        return self

    async def __aexit__(self, *errors):
        if not self.session.closed:
            await self.session.close()
        self.session = None

    async def close(self) -> None:
        ''' Closes the internal aiohttp ClientSession. Use this if BotrixClient isn't being used as an async context manager. '''
        if self.session:
            await self.session.close()

    async def _handle_response(self, resp) -> None:
        status = resp.status
        if self.debug:
            print('BOTRIX DEBUG MODE\n', await resp.json(), '\n')
        if status == 429:
            data = await resp.json()
            raise RatelimitException(data.get('message') or data.get('ERROR', str(data)))
        elif status == 404:
            raise BotrixException('404')
    

    async def get_bot(self, bot_id) -> Bot:
        ''' Returns an instance of botrix.Bot containing information of the given bot. If the bot is not found, the boolean value of the returned instance of botrix.Bot will be False. '''
        async with self.session.get(f'{self.BASE_URL}/bot/{bot_id}') as resp:
            await self._handle_response(resp)
            data = await resp.json()
        return Bot(data)

    async def check_vote(self, bot_id, user_id) -> bool:
        ''' Checks if User with `user_id` has voted for Bot with `bot_id` '''
        async with self.session.get(f'{self.BASE_URL}/voted/{bot_id}/{user_id}') as resp:
            await self._handle_response(resp)
            data = await resp.json()
        if 'voted' in data:
            return data['voted']
        else:
            raise BotrixException(data.get('ERROR'))
        
    async def post_bot_data(self, bot_id, **kwargs) -> dict:
        ''' POSTs data from given kwargs to the bot of `bot_id`. Valid kwargs are: `servers`, `shards`, `users` '''
        async with self.session.post(f'{self.BASE_URL}/bot/{bot_id}', data=kwargs) as resp:
            await self._handle_response(resp)
            data = await resp.json()
        return data
        

