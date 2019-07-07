import only_otters.resourcely as rly

from argparse import Namespace

__resources__: Namespace = rly.from_located_file(near=__file__)
rly.expand(__resources__, globals())
