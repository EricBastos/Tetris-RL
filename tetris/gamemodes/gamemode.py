from abc import ABC, abstractmethod


class GameMode(ABC):

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        pass

    @abstractmethod
    def render(self):
        pass
