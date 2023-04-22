from discord.ext import commands


class DisplayNameMemberConverter(commands.MemberConverter):
    async def convert(self, ctx, argument):
        for member in ctx.guild.members:
            if member.display_name.lower() == argument.lower():
                return member
        raise commands.MemberNotFound(argument)
