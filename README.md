# botrix

An API Wrapper that supports asynchronous requests for the [Botrix API](https://docs.botrix.cc/)


# Usage

> Using BotrixClient as a context manager

```py
import asyncio
from botrix import BotrixClient

async def main():
    async with BotrixClient() as client:
        bot = await client.get_bot(751100444188737617)
        print(bot.votes)

asyncio.get_event_loop().run_until_complete(main())
```

> Closing the session manually
```py
import asyncio
from botrix import BotrixClient

async def main():
    client = BotrixClient()
    bot = await client.get_bot(751100444188737617)
    print(bot.votes)
    await client.close()

asyncio.get_event_loop().run_until_complete(main())
```
