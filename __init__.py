from .process_proposals import ProcessProposals


def setup(bot):
    bot.add_cog(ProcessProposals(bot))
