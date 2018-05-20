

class EventManager():
    def __init__(self, application):
        self.observer_list = []
        self.application = application

    def register(self, observer: "Type: Observer"):
        self.observer.append(observer)

    def connect(self, connector):
        self.application.connector()

    def on_click(self, *args):
        map(lambda obs: obs.execute("on_click"), self.observer_list)

    def on_motion(self, *args):
        map(lambda obs: obs.execute("on_motion"), self.observer_list)

    def on_release(self, *args):
        map(lambda obs: obs.execute("on_release"), self.observer_list)
