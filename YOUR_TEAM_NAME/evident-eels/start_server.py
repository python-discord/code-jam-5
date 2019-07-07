import os
import string
import random

if __name__ == "__main__":
    os.environ["SECRET_KEY"] = "".join(random.choices([char for char in string.printable if char not in string.whitespace], k=15))
    import carpool
    carpool.run()