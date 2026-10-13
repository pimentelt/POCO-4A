"""
ATIVIDADE EM SALA — GUI com Padrões de Projeto
Domínio: planejamento de atividades acadêmicas.

Classes de domínio:
- Atividade: valida título, horas estimadas e prioridade; lança ValueError quando inválidos.
- EstrategiaPrioridade, PrioridadeAlta e PrioridadeNormal: encapsulam recomendações.
- Notificador: avisa observadores quando uma atividade é cadastrada.
- Aplicacao: cria a interface Tkinter e converte erros de validação em diálogos.

Dados validados:
- Título não vazio.
- Horas estimadas maiores que zero e no máximo 200.
- Prioridade inteira entre 1 e 5.

Padrões escolhidos:
1. Strategy: permite variar a recomendação sem misturar essa regra à interface.
2. Observer: notifica a interface após o cadastro sem acoplar o cadastro diretamente
   ao componente que exibe a lista.

Uso de IA: apoio à estruturação inicial do código e à documentação dos padrões.
Revise e adapte este registro para refletir exatamente o uso que fez da ferramenta.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class Atividade:
    """Objeto de domínio responsável por validar os dados do cadastro."""

    def __init__(self, titulo: str, horas: str, prioridade: str):
        titulo = titulo.strip()
        if not titulo:
            raise ValueError("Informe o nome da atividade.")

        try:
            horas_num = float(horas.replace(",", "."))
        except (ValueError, AttributeError):
            raise ValueError("As horas devem ser um número válido.") from None
        if not 0 < horas_num <= 200:
            raise ValueError("As horas devem ser maiores que 0 e no máximo 200.")

        try:
            prioridade_num = int(prioridade)
        except (ValueError, TypeError):
            raise ValueError("A prioridade deve ser um número inteiro de 1 a 5.") from None
        if not 1 <= prioridade_num <= 5:
            raise ValueError("A prioridade deve estar entre 1 e 5.")

        self.titulo = titulo
        self.horas = horas_num
        self.prioridade = prioridade_num


# PADRÃO STRATEGY
# Nome: Strategy.
# Problema: recomendações diferentes poderiam ficar espalhadas em condicionais da GUI.
# Solução: cada estratégia implementa a operação recomendar() de uma forma.
# Consequências: novas recomendações podem ser adicionadas sem alterar a interface;
# para regras muito simples, isso cria classes extras e pode aumentar a complexidade.
class EstrategiaPrioridade:
    def recomendar(self, atividade: Atividade) -> str:
        raise NotImplementedError


class PrioridadeAlta(EstrategiaPrioridade):
    def recomendar(self, atividade: Atividade) -> str:
        return "Prioridade alta: reserve um bloco de tempo para esta atividade."


class PrioridadeNormal(EstrategiaPrioridade):
    def recomendar(self, atividade: Atividade) -> str:
        return "Inclua esta atividade no planejamento semanal."


def obter_estrategia(atividade: Atividade) -> EstrategiaPrioridade:
    if atividade.prioridade >= 4:
        return PrioridadeAlta()
    return PrioridadeNormal()


# PADRÃO OBSERVER
# Nome: Observer.
# Problema: o cadastro não deve conhecer diretamente todos os componentes que reagem a ele.
# Solução: Notificador mantém callbacks inscritos e os chama quando há novo cadastro.
# Consequências: outros observadores podem ser incluídos sem mudar o cadastro; por outro
# lado, a ordem das notificações segue a inscrição e falhas em callbacks exigiriam tratamento.
class Notificador:
    def __init__(self):
        self._observadores = []

    def inscrever(self, callback):
        self._observadores.append(callback)

    def notificar(self, atividade: Atividade):
        for callback in self._observadores:
            callback(atividade)


class Aplicacao:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Planejador de Atividades Acadêmicas")
        self.raiz.minsize(520, 390)

        self.notificador = Notificador()
        self.notificador.inscrever(self.atualizar_lista)

        principal = ttk.Frame(raiz, padding=18)
        principal.grid(row=0, column=0, sticky="nsew")
        raiz.columnconfigure(0, weight=1)
        raiz.rowconfigure(0, weight=1)
        principal.columnconfigure(1, weight=1)

        ttk.Label(
            principal, text="Cadastro de atividade",
            font=("TkDefaultFont", 15, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

        ttk.Label(principal, text="Nome da atividade:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.campo_titulo = ttk.Entry(principal)
        self.campo_titulo.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(principal, text="Horas estimadas:").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.campo_horas = ttk.Entry(principal)
        self.campo_horas.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(principal, text="Prioridade (1 a 5):").grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.campo_prioridade = ttk.Spinbox(principal, from_=1, to=5, width=8)
        self.campo_prioridade.set("3")
        self.campo_prioridade.grid(row=3, column=1, sticky="w", pady=5)

        ttk.Button(
            principal, text="Cadastrar atividade", command=self.cadastrar
        ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 14))

        ttk.Label(
            principal, text="Atividades cadastradas:",
            font=("TkDefaultFont", 10, "bold")
        ).grid(row=5, column=0, columnspan=2, sticky="w")

        self.lista = tk.Listbox(principal, height=7)
        self.lista.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=(5, 8))
        principal.rowconfigure(6, weight=1)

        self.status = ttk.Label(
            principal, text="Preencha os campos para começar.", wraplength=470
        )
        self.status.grid(row=7, column=0, columnspan=2, sticky="w")

    def cadastrar(self):
        # A validação é feita no domínio, não repetida dentro da interface.
        try:
            atividade = Atividade(
                self.campo_titulo.get(),
                self.campo_horas.get(),
                self.campo_prioridade.get()
            )
        except ValueError as erro:
            messagebox.showerror("Dados inválidos", str(erro), parent=self.raiz)
            return

        self.notificador.notificar(atividade)
        self.status.config(text=obter_estrategia(atividade).recomendar(atividade))
        self.campo_titulo.delete(0, tk.END)
        self.campo_horas.delete(0, tk.END)
        self.campo_prioridade.set("3")

    def atualizar_lista(self, atividade):
        self.lista.insert(
            tk.END,
            f"{atividade.titulo} — {atividade.horas:g} h — prioridade {atividade.prioridade}"
        )


if __name__ == "__main__":
    janela = tk.Tk()
    Aplicacao(janela)
    janela.mainloop()


# AUTOAVALIAÇÃO — preencher após executar e testar:
# 1. Critérios atingidos/não atingidos: confira os seis critérios do enunciado.
# 2. Trecho mais trabalhoso e solução: registre sua experiência real.
# 3. Consequências dos padrões: confirme se Strategy e Observer se comportaram como descrito.
# 4. Uso de IA: registre honestamente em que ajudou e em que atrapalhou.
