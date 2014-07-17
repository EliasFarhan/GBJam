from render_engine.img_manager import img_manager


class Scene():
    def __init__(self):
        pass

    def init(self, loading=False):
        pass

    def loop(self, screen):
        pass

    def exit(self):
        img_manager.sanitize_img_manager()