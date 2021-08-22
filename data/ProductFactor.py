

class ProductFactor():

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.value = 1
        self._observers = []

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def attach(self, observer):
        self._observers.append(observer)

    def set(self, value):
        self.value = value
        self.notify()
