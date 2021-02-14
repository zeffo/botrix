import aiohttp

class Bot:
    def __init__(self, data):
        bot = data.get('bot')
        for attr, value in bot.items():
            setattr(self, attr, value)

class BotrixClient:
    def __init__(self, *, loop):
        self.session = aiohttp.ClientSession(loop=loop)
    
    async def get_bot(self, _id):
        resp = await self.session.get(f'https://botrix.cc/api/v1/bot/{_id}')
        data = await resp.json()
        return Bot(data)

    async def check_vote(self, bot_id, user_id):
        resp = await self.session.get(f'https://botrix.cc/api/v1/voted/{bot_id}/{user_id}')
        data = await resp.json()
        return data.get('voted')
