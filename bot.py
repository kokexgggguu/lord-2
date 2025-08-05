#!/usr/bin/env python3
"""
Complete Discord Bot with All Commands
"""
import asyncio
import os
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import random
import sqlite3
import logging

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Simple logging function
def log_command_usage(user_id, guild_id, command, details=""):
    """Simple command logging"""
    print(f"[{datetime.now()}] User {user_id} in guild {guild_id} used /{command}: {details}")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

# Basic Commands
@bot.tree.command(name="ping", description="Check bot latency and status")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: **{latency}ms**",
        color=0x00ff00,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="Status", value="Online", inline=True)
    embed.add_field(name="Servers", value=str(len(bot.guilds)), inline=True)
    
    await interaction.response.send_message(embed=embed)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "ping")

@bot.tree.command(name="serverinfo", description="Display server information")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    
    embed = discord.Embed(
        title=f"📊 {guild.name} Server Information",
        color=0x0099ff,
        timestamp=datetime.utcnow()
    )
    
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Created", value=f"<t:{int(guild.created_at.timestamp())}:F>", inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)
    
    await interaction.response.send_message(embed=embed)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "serverinfo")

@bot.tree.command(name="userinfo", description="Show user information")
@discord.app_commands.describe(member="The member to get info about")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user
    
    # Ensure we have a guild member
    if not isinstance(member, discord.Member):
        await interaction.response.send_message("❌ This command only works in servers.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title=f"👤 {member.display_name}",
        color=member.color if member.color != discord.Color.default() else 0x0099ff,
        timestamp=datetime.utcnow()
    )
    
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="Username", value=str(member), inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=f"<t:{int(member.joined_at.timestamp())}:F>" if member.joined_at else "Unknown", inline=True)
    embed.add_field(name="Account Created", value=f"<t:{int(member.created_at.timestamp())}:F>", inline=True)
    embed.add_field(name="Roles", value=f"{len(member.roles)-1} roles", inline=True)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    
    await interaction.response.send_message(embed=embed)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "userinfo", f"Target: {member}")

@bot.tree.command(name="avatar", description="Display user's avatar")
@discord.app_commands.describe(member="The member to show avatar for")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user
    
    # Handle both Member and User types
    target_member = member if isinstance(member, discord.Member) else interaction.user
    
    embed = discord.Embed(
        title=f"🖼️ {target_member.display_name}'s Avatar",
        color=target_member.color if hasattr(target_member, 'color') and target_member.color != discord.Color.default() else 0x0099ff,
        timestamp=datetime.utcnow()
    )
    
    avatar_url = target_member.avatar.url if target_member.avatar else target_member.default_avatar.url
    embed.set_image(url=avatar_url)
    embed.add_field(name="Direct Link", value=f"[Click here]({avatar_url})", inline=False)
    
    await interaction.response.send_message(embed=embed)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "avatar", f"Target: {member}")

@bot.tree.command(name="8ball", description="Ask the magic 8-ball")
@discord.app_commands.describe(question="Your question for the 8-ball")
async def eight_ball(interaction: discord.Interaction, question: str):
    responses = [
        "It is certain", "It is decidedly so", "Without a doubt", "Yes definitely",
        "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
        "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
        "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
        "Don't count on it", "My reply is no", "My sources say no",
        "Outlook not so good", "Very doubtful"
    ]
    
    embed = discord.Embed(
        title="🎱 Magic 8-Ball",
        color=0x8B0000,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="Question", value=question, inline=False)
    embed.add_field(name="Answer", value=random.choice(responses), inline=False)
    embed.set_footer(text=f"Asked by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "8ball", f"Question: {question}")

# Utility Commands
@bot.tree.command(name="say", description="Make the bot say something")
@discord.app_commands.describe(message="The message to say", channel="Channel to send to (optional)")
async def say(interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    
    target_channel = channel or interaction.channel
    
    try:
        await target_channel.send(message)
        
        embed = discord.Embed(
            title="✅ Message Sent",
            description=f"Message sent to {target_channel.mention}",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Message", value=message[:1000] + "..." if len(message) > 1000 else message, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        log_command_usage(str(interaction.user.id), str(interaction.guild.id), "say", f"Channel: {target_channel.name}")
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to send messages in that channel.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error occurred: {str(e)}", ephemeral=True)

@bot.tree.command(name="embed", description="Create custom embed messages")
@discord.app_commands.describe(title="Embed title", description="Embed description", color="Hex color (e.g., #ff0000)")
async def embed_command(interaction: discord.Interaction, title: str, description: str, color: str = "#0099ff"):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    
    try:
        # Parse color
        color_int = int(color.replace("#", ""), 16) if color.startswith("#") else int(color, 16)
    except ValueError:
        color_int = 0x0099ff
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=color_int,
        timestamp=datetime.utcnow()
    )
    
    embed.set_footer(text=f"Created by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "embed", f"Title: {title}")

@bot.tree.command(name="roleinfo", description="Show detailed role information")
@discord.app_commands.describe(role="The role to get information about")
async def roleinfo(interaction: discord.Interaction, role: discord.Role):
    embed = discord.Embed(
        title=f"📋 Role Information: {role.name}",
        color=role.color if role.color != discord.Color.default() else 0x0099ff,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="Name", value=role.name, inline=True)
    embed.add_field(name="ID", value=role.id, inline=True)
    embed.add_field(name="Color", value=str(role.color), inline=True)
    embed.add_field(name="Position", value=role.position, inline=True)
    embed.add_field(name="Members", value=len(role.members), inline=True)
    embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
    embed.add_field(name="Hoisted", value="Yes" if role.hoist else "No", inline=True)
    embed.add_field(name="Managed", value="Yes" if role.managed else "No", inline=True)
    embed.add_field(name="Created", value=f"<t:{int(role.created_at.timestamp())}:F>", inline=True)
    
    # Show some key permissions
    perms = []
    if role.permissions.administrator:
        perms.append("Administrator")
    if role.permissions.manage_guild:
        perms.append("Manage Server")
    if role.permissions.manage_channels:
        perms.append("Manage Channels")
    if role.permissions.manage_messages:
        perms.append("Manage Messages")
    if role.permissions.kick_members:
        perms.append("Kick Members")
    if role.permissions.ban_members:
        perms.append("Ban Members")
    
    if perms:
        embed.add_field(name="Key Permissions", value=", ".join(perms[:5]), inline=False)
    
    await interaction.response.send_message(embed=embed)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "roleinfo", f"Role: {role.name}")

@bot.tree.command(name="channelinfo", description="Show channel information")
@discord.app_commands.describe(channel="The channel to get info about")
async def channelinfo(interaction: discord.Interaction, channel: discord.TextChannel = None):
    if channel is None:
        channel = interaction.channel
    
    embed = discord.Embed(
        title=f"📺 Channel Information: #{channel.name}",
        color=0x0099ff,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="Name", value=channel.name, inline=True)
    embed.add_field(name="ID", value=channel.id, inline=True)
    embed.add_field(name="Type", value=str(channel.type).title(), inline=True)
    embed.add_field(name="Category", value=channel.category.name if channel.category else "None", inline=True)
    embed.add_field(name="Position", value=channel.position, inline=True)
    embed.add_field(name="NSFW", value="Yes" if channel.is_nsfw() else "No", inline=True)
    embed.add_field(name="Created", value=f"<t:{int(channel.created_at.timestamp())}:F>", inline=True)
    
    if channel.topic:
        embed.add_field(name="Topic", value=channel.topic[:1000], inline=False)
    
    await interaction.response.send_message(embed=embed)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "channelinfo", f"Channel: {channel.name}")

# Moderation Commands
@bot.tree.command(name="kick", description="Kick a member from server")
@discord.app_commands.describe(member="The member to kick", reason="Reason for kick")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("❌ You don't have permission to kick members.", ephemeral=True)
        return
    
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ You cannot kick this member (role hierarchy).", ephemeral=True)
        return
    
    try:
        await member.kick(reason=reason)
        
        embed = discord.Embed(
            title="👢 Member Kicked",
            color=0xff6b6b,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Member", value=f"{member.mention} ({member})", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        
        await interaction.response.send_message(embed=embed)
        log_command_usage(str(interaction.user.id), str(interaction.guild.id), "kick", f"Kicked {member}: {reason}")
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to kick this member.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error occurred: {str(e)}", ephemeral=True)

@bot.tree.command(name="ban", description="Ban a member from server")
@discord.app_commands.describe(member="The member to ban", reason="Reason for ban", delete_days="Days of message history to delete (0-7)")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided", delete_days: int = 0):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ You don't have permission to ban members.", ephemeral=True)
        return
    
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ You cannot ban this member (role hierarchy).", ephemeral=True)
        return
    
    if delete_days < 0 or delete_days > 7:
        await interaction.response.send_message("❌ Delete days must be between 0 and 7.", ephemeral=True)
        return
    
    try:
        await member.ban(reason=reason, delete_message_days=delete_days)
        
        embed = discord.Embed(
            title="🔨 Member Banned",
            color=0xff0000,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Member", value=f"{member.mention} ({member})", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Messages Deleted", value=f"{delete_days} days", inline=True)
        
        await interaction.response.send_message(embed=embed)
        log_command_usage(str(interaction.user.id), str(interaction.guild.id), "ban", f"Banned {member}: {reason}")
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to ban this member.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error occurred: {str(e)}", ephemeral=True)

@bot.tree.command(name="clear", description="Clear messages from channel")
@discord.app_commands.describe(amount="Number of messages to clear (1-100)")
async def clear(interaction: discord.Interaction, amount: int = 5):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You don't have permission to manage messages.", ephemeral=True)
        return
    
    if amount < 1 or amount > 100:
        await interaction.response.send_message("❌ Please specify a number between 1 and 100.", ephemeral=True)
        return
    
    try:
        deleted = await interaction.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="🧹 Messages Cleared",
            description=f"Successfully deleted {len(deleted)} messages.",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Cleared by", value=interaction.user.mention, inline=True)
        embed.add_field(name="Amount", value=str(len(deleted)), inline=True)
        
        await interaction.response.send_message(embed=embed, delete_after=5)
        log_command_usage(str(interaction.user.id), str(interaction.guild.id), "clear", f"Cleared {len(deleted)} messages")
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to delete messages in this channel.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error occurred: {str(e)}", ephemeral=True)

@bot.tree.command(name="unban", description="Unban a user by ID")
@discord.app_commands.describe(user_id="The ID of the user to unban", reason="Reason for unban")
async def unban(interaction: discord.Interaction, user_id: str, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ You don't have permission to unban members.", ephemeral=True)
        return
    
    try:
        user_id_int = int(user_id)
        user = await bot.fetch_user(user_id_int)
        
        await interaction.guild.unban(user, reason=reason)
        
        embed = discord.Embed(
            title="✅ User Unbanned",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="User", value=f"{user.mention} ({user})", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        
        await interaction.response.send_message(embed=embed)
        log_command_usage(str(interaction.user.id), str(interaction.guild.id), "unban", f"Unbanned {user}: {reason}")
        
    except discord.NotFound:
        await interaction.response.send_message("❌ User not found or not banned.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to unban users.", ephemeral=True)
    except ValueError:
        await interaction.response.send_message("❌ Invalid user ID provided.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error occurred: {str(e)}", ephemeral=True)

@bot.tree.command(name="timeout", description="Timeout a member")
@discord.app_commands.describe(member="The member to timeout", duration="Duration in minutes", reason="Reason for timeout")
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ You don't have permission to timeout members.", ephemeral=True)
        return
    
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ You cannot timeout this member (role hierarchy).", ephemeral=True)
        return
    
    if duration < 1 or duration > 40320:  # Discord max is 28 days
        await interaction.response.send_message("❌ Duration must be between 1 minute and 28 days (40320 minutes).", ephemeral=True)
        return
    
    try:
        timeout_until = datetime.utcnow() + timedelta(minutes=duration)
        await member.timeout(timeout_until, reason=reason)
        
        embed = discord.Embed(
            title="⏰ Member Timed Out",
            color=0xffa500,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Member", value=f"{member.mention} ({member})", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
        embed.add_field(name="Until", value=f"<t:{int(timeout_until.timestamp())}:F>", inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        
        await interaction.response.send_message(embed=embed)
        log_command_usage(str(interaction.user.id), str(interaction.guild.id), "timeout", f"Timed out {member} for {duration} minutes: {reason}")
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to timeout this member.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error occurred: {str(e)}", ephemeral=True)

@bot.tree.command(name="untimeout", description="Remove timeout from member")
@discord.app_commands.describe(member="The member to remove timeout from", reason="Reason for removing timeout")
async def untimeout(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ You don't have permission to manage timeouts.", ephemeral=True)
        return
    
    if not member.is_timed_out():
        await interaction.response.send_message("❌ This member is not timed out.", ephemeral=True)
        return
    
    try:
        await member.timeout(None, reason=reason)
        
        embed = discord.Embed(
            title="✅ Timeout Removed",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Member", value=f"{member.mention} ({member})", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        
        await interaction.response.send_message(embed=embed)
        log_command_usage(str(interaction.user.id), str(interaction.guild.id), "untimeout", f"Removed timeout from {member}: {reason}")
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to remove timeout from this member.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error occurred: {str(e)}", ephemeral=True)

@bot.tree.command(name="warn", description="Warn a member (with DM)")
@discord.app_commands.describe(member="The member to warn", reason="Reason for warning")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You don't have permission to warn members.", ephemeral=True)
        return
    
    try:
        # Try to send DM to user
        dm_sent = False
        try:
            dm_embed = discord.Embed(
                title="⚠️ Warning",
                description=f"You have been warned in **{interaction.guild.name}**",
                color=0xffaa00,
                timestamp=datetime.utcnow()
            )
            dm_embed.add_field(name="Reason", value=reason, inline=False)
            dm_embed.add_field(name="Moderator", value=str(interaction.user), inline=True)
            
            await member.send(embed=dm_embed)
            dm_sent = True
        except discord.Forbidden:
            pass
        
        # Send public warning
        embed = discord.Embed(
            title="⚠️ Member Warned",
            color=0xffaa00,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Member", value=f"{member.mention} ({member})", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="DM Sent", value="Yes" if dm_sent else "No (DMs disabled)", inline=True)
        
        await interaction.response.send_message(embed=embed)
        log_command_usage(str(interaction.user.id), str(interaction.guild.id), "warn", f"Warned {member}: {reason}")
        
    except Exception as e:
        await interaction.response.send_message(f"❌ Error occurred: {str(e)}", ephemeral=True)

# Match Management Commands
@bot.tree.command(name="create_match", description="Create scheduled matches")
@discord.app_commands.describe(team1="First team name", team2="Second team name", time="Match time (e.g., '14:30')", description="Match description")
async def create_match(interaction: discord.Interaction, team1: str, team2: str, time: str, description: str = "No description"):
    if not interaction.user.guild_permissions.manage_events:
        await interaction.response.send_message("❌ You don't have permission to create matches.", ephemeral=True)
        return
    
    try:
        # Simple match creation without database for now
        match_id = random.randint(1000, 9999)
        
        embed = discord.Embed(
            title="⚽ Match Created",
            description=f"**{team1}** vs **{team2}**",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Match ID", value=str(match_id), inline=True)
        embed.add_field(name="Time", value=time, inline=True)
        embed.add_field(name="Created by", value=interaction.user.mention, inline=True)
        embed.add_field(name="Description", value=description, inline=False)
        
        await interaction.response.send_message(embed=embed)
        log_command_usage(str(interaction.user.id), str(interaction.guild.id), "create_match", f"{team1} vs {team2} at {time}")
        
    except Exception as e:
        await interaction.response.send_message(f"❌ Error occurred: {str(e)}", ephemeral=True)

@bot.tree.command(name="list_matches", description="List active matches")
async def list_matches(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚽ Active Matches",
        description="No active matches found.",
        color=0x0099ff,
        timestamp=datetime.utcnow()
    )
    
    # This would normally fetch from database
    embed.add_field(name="Info", value="Use `/create_match` to create new matches", inline=False)
    
    await interaction.response.send_message(embed=embed)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "list_matches")

@bot.tree.command(name="end_match", description="End a match by ID")
@discord.app_commands.describe(match_id="The ID of the match to end")
async def end_match(interaction: discord.Interaction, match_id: int):
    if not interaction.user.guild_permissions.manage_events:
        await interaction.response.send_message("❌ You don't have permission to end matches.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="✅ Match Ended",
        description=f"Match #{match_id} has been ended.",
        color=0x00ff00,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="Ended by", value=interaction.user.mention, inline=True)
    
    await interaction.response.send_message(embed=embed)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "end_match", f"Ended match #{match_id}")

@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Bot Commands Help",
        description="Here are all available commands:",
        color=0x0099ff,
        timestamp=datetime.utcnow()
    )
    
    # Basic Commands
    embed.add_field(
        name="🔧 Basic Commands",
        value=(
            "`/ping` - Check bot latency\n"
            "`/help` - Show this help message\n"
            "`/serverinfo` - Get server information\n"
            "`/userinfo` - Get user information\n"
            "`/avatar` - Show user's avatar\n"
            "`/8ball` - Ask the magic 8-ball"
        ),
        inline=False
    )
    
    # Moderation Commands (if user has permissions)
    if interaction.user.guild_permissions.manage_messages:
        embed.add_field(
            name="🛡️ Moderation Commands",
            value=(
                "`/kick` - Kick a member\n"
                "`/ban` - Ban a member\n"
                "`/unban` - Unban a user by ID\n"
                "`/timeout` - Timeout a member\n"
                "`/untimeout` - Remove timeout\n"
                "`/warn` - Warn a member (with DM)\n"
                "`/clear` - Clear messages"
            ),
            inline=False
        )
    
    # Utility Commands
    embed.add_field(
        name="🔧 Utility Commands",
        value=(
            "`/say` - Make bot say something\n"
            "`/embed` - Create custom embed\n"
            "`/roleinfo` - Show role information\n"
            "`/channelinfo` - Show channel info"
        ),
        inline=False
    )
    
    # Match Commands  
    embed.add_field(
        name="⚽ Match Commands",
        value=(
            "`/create_match` - Create a match\n"
            "`/list_matches` - List active matches\n"
            "`/end_match` - End a match"
        ),
        inline=False
    )
    
    embed.set_footer(text="Made by kokex | Discord Bot v2.0")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    log_command_usage(str(interaction.user.id), str(interaction.guild.id), "help")

# Bot run function
async def run_bot():
    """Main function to run the Discord bot"""
    if not TOKEN:
        print("DISCORD_TOKEN environment variable not set!")
        return
    
    try:
        await bot.start(TOKEN)
    except discord.LoginFailure:
        print("Invalid bot token!")
    except Exception as e:
        print(f"Bot error: {e}")

if __name__ == "__main__":
    asyncio.run(run_bot())