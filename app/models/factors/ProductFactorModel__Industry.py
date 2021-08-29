from .ProductFactors import ProductFactorModel


class ProductFactorModel__Industry(ProductFactorModel):
    def __init__(self, id, name, config, *args, **kwargs):
        self.id = id
        self.name = name
        self.config = config

    def set(self, selection):
        self.value = 0.9
