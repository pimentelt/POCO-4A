## @file atividade02.py

# Tamagotchi
# Atividade sobre herança, polimorfismo e encapsulamento.

class Pet:
    def __init__(self, nome, idade=0):
        self.__nome = nome
        self.__idade = idade

        # O construtor utiliza os setters para validar os valores.
        self.felicidade = 10
        self.fome = 10
        self.__energia = 10
        self.__conhecimento = 0
        self.__estresse = 0

    @property
    def nome(self):
        return self.__nome

    @property
    def idade(self):
        return self.__idade

    @property
    def felicidade(self):
        return self.__felicidade

    @felicidade.setter
    def felicidade(self, valor):
        if valor < 0 or valor > 10:
            raise ValueError("A felicidade deve estar entre 0 e 10!")
        self.__felicidade = valor
    
    @property
    def fome(self):
        return self.__fome

    @fome.setter
    def fome(self, valor):
        if valor < 0 or valor > 10:
            raise ValueError("A fome deve estar entre 0 e 10!")
        self.__fome = valor

    def agir(self):
        raise NotImplementedError

    def alimentar(self):
        self.fome = 10
        print(f"{self.nome} foi alimentado.")


class PetEstudioso(Pet):
    def __init__(self, nome, idade, materia_favorita):
        super().__init__(nome, idade)
        self.materia_favorita = materia_favorita

    def agir(self):
        print(f"{self.nome} estudou {self.materia_favorita}!")

    def alimentar(self):
        super().alimentar()
        print(f"{self.nome} ganhou energia para estudar.")


class PetPreguicoso(Pet):
    def __init__(self, nome, idade, horas_sono):
        super().__init__(nome, idade)
        self.horas_sono = horas_sono

    def agir(self):
        print(f"{self.nome} dormiu por {self.horas_sono} horas!")

    def alimentar(self):
        super().alimentar()
        print(f"{self.nome} ficou satisfeito e voltou a dormir.")


class Jogador:
    def __init__(self, nome, pet):
        self.__nome = nome
        self.__pet = pet

    @property
    def nome(self):
        return self.__nome

    @property
    def pet(self):
        return self.__pet


# =========================
# Demonstração do programa
# =========================

print("=== TAMAGOTCHI ===")

pet1 = PetEstudioso("Bob", 3, "Álgebra Linear")
pet2 = PetPreguicoso("Mimi", 2, 8)

jogador1 = Jogador("Tarsila", pet1)

print("\n--- Criações válidas ---")
print(f"Pet 1: {pet1.nome}, {pet1.idade} anos")
print(f"Pet 2: {pet2.nome}, {pet2.idade} anos")
print(f"Jogador: {jogador1.nome}")
print(f"Pet do jogador: {jogador1.pet.nome}")

print("\n--- Polimorfismo ---")

pets = [pet1, pet2]

for pet in pets:
    print(f"\nPet: {pet.nome}")
    pet.agir()
    pet.alimentar()


print("\n--- Teste de validação ---")

try:
    pet1.felicidade = 15
except ValueError as erro:
    print(f"Recusa: {erro}")

try:
    pet1.fome = -2
except ValueError as erro:
    print(f"Recusa: {erro}")

print("\n--- Estado do Bob ---")
print(f"Felicidade: {pet1.felicidade}")
print(f"Fome: {pet1.fome}")
