from .blended_wrapper import BlendedWrapper

BlendedAverageWrapper = BlendedWrapper
'''
. means:

"Look in the current package/directory."

So Python interprets it as:

I'm currently inside: src.ensemble.wrappers

Go to:
src.ensemble.wrappers.blended_wrapper

and get:
BlendedWrapper

It's roughly equivalent to:

from src.ensemble.wrappers.blended_wrapper import BlendedWrapper
'''