from .ProductFactors import ProductFactorModel


class ProductFactorModel__GroupSize(ProductFactorModel):
    def __init__(self, id, name, config, *args, **kwargs):
        self.id = id
        self.name = name
        self.config = config

    def set(self, selection):
        if selection is None:
            raise ValueError("payload must contain a `groupsize` key")
        groupsize = selection

        if type(groupsize) != int:
            raise ValueError("groupsize must be an integer")
        elif groupsize < 250:
            self.value = 1
        elif groupsize < 500:
            self.value = 0.95
        elif groupsize < 1000:
            self.value = 0.9
        else:
            self.value = 0.8
