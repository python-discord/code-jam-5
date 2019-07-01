import tests.blocks as block


blocks_file = block.test_file()

if blocks_file is True:
    block.test_cards(0.1)
