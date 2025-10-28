class Veicolo:
    def __init__(self, marca, modello, anno):
        self.marca = marca
        self.modello = modello
        self.anno = anno

    def descrizione(self):
        return f"{self.anno} {self.marca} {self.modello}"

class Moto(Veicolo):
    def __init__(self, marca, modello, anno, tipo):
        super().__init__(marca, modello, anno)
        self.tipo = tipo

    def descrizione(self):
        base_descrizione = super().descrizione()
        return f"{base_descrizione}, Tipo: {self.tipo}"