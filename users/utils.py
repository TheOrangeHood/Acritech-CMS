import random, string


def random_alphanumeric_generator(size=6):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=size))
