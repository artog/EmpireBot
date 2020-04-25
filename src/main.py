import asyncio
import discord
from discord.ext import commands
ffmpeg_options = {
    'options': '-vn'
}

#bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"),
#                   description='Wololo')



class EmpireBot(commands.Bot):
    async def on_ready(self):
        self.voice_client = None
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        ctx = await self.get_context(message)

        cmd, *args = message.content.split()

        if message.content.startswith('!join'):
            if len(args) < 1:
                await ctx.send("Missing argument. Syntax: !join <channel>")
                return

            await self.join(ctx, channel_name=" ".join(args))

        if message.content.lower() == "general kenobi":
            await message.channel.send("Hello there!")

        if message.content.lower() == "!stop":
            await self.stop(ctx)

        if message.content.startswith("!volume"):

            if len(args) < 1:
                await ctx.send("Missing argument. Syntax: !volume <level>")
                return

            await self.volume(ctx, volume=int(args[0]))

        if message.content.startswith("!play"):
            try:
                await self.ensure_voice(ctx)
                await self.play(ctx, query=" ".join(args))
            except commands.CommandError:
                pass

        if message.content in [str(i) for i in range(1,43)]:
            await self.ensure_voice(ctx)
            await self.play(ctx, query=f"sounds/aoe_{message.content}.ogg")

    async def join(self, ctx, *, channel_name: str):
        """Joins a voice channel"""
        channels = [c for c in self.get_all_channels() if c.type.name == "voice" and c.name == channel_name]

        if len(channels) != 1:
            await ctx.send(f"Unknown channel: {channel_name}")
            return

        channel = channels[0]

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        if ctx.voice_client != None:
            await ctx.voice_client.disconnect()

    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


bot = EmpireBot("!")
bot.run('NzAzMTIzNzIxNDc2NjM2NzMz.XqKBKw.DpFDfAMZyKhXAyj-mKpnaUUXmKE')