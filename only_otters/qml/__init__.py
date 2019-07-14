import only_otters.resourcely as rly


__resources__ = rly.from_located_file(near=__file__)
rly.expand(__resources__, globals())
