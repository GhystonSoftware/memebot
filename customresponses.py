from addtext import add_text
import random

def pub_response():
    options = [
        ('kitten', 'PUB!?')
    ]
    chosen_meme = random.choice(options)
    return add_text(*chosen_meme)

phrases = {
    'pub?': pub_response
}
