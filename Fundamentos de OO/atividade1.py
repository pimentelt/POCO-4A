## @file atividade01.py

# Tamagotchi
# Atividade sobre classes, construtores e encapsulamento.

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

# Primeira forma de criação: informando nome e idade.
pet1 = Pet("Bob", 3)

# Segunda forma de criação: usando a idade padrão (0).
pet2 = Pet("Mimi")

# A classe Jogador recebe um objeto da classe Pet.
jogador1 = Jogador("Tarsila", pet1)

print("\n--- Criações válidas ---")
print(f"Pet 1: {pet1.nome}, {pet1.idade} anos")
print(f"Pet 2: {pet2.nome}, {pet2.idade} anos")
print(f"Jogador: {jogador1.nome}")
print(f"Pet do jogador: {jogador1.pet.nome}")

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
