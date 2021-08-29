import abc


class ProductFactorModel(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set(self):
        pass
