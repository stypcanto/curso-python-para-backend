class Perro:
    def __init__(self, peso: float, talla: float, familia: str):
        self.peso = peso
        self.talla = talla
        self.familia = familia
        
perro_golden = Perro(15.5, 2.20, "Golden")
perro_salchicha = Perro(2.2, 1.2, "Salchicha")
perro_san_bernardo = Perro(15.3, 2604, "San Bernardo")
    
print(perro_golden.peso,perro_golden.talla,perro_golden.familia)