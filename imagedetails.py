class ImageDetails:
    def __init__(self, img_path, location, size, font='FjallaOne-Regular.ttf', color=(255, 255, 255), rotation=0, is_gif=False):
        self.path = 'photos/{}'.format(img_path)
        self.location = location
        self.size = size
        self.font = 'fonts/{}'.format(font)
        self.color = color
        self.rotation = rotation
        self.is_gif = is_gif
