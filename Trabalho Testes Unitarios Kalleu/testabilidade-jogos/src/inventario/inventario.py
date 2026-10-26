"""MODEL: lógica pura do inventário. Não conhece Unity/Godot/tela/nada de engine."""
from .excecoes import InventarioCheioError, ItemInsuficienteError


class Inventario:
    def __init__(self, capacidade: int):
        if capacidade <= 0:
            raise ValueError("capacidade deve ser maior que zero")
        self.capacidade = capacidade
        self._itens: dict[str, int] = {}

    # ---------- consultas ----------
    @property
    def total(self) -> int:
        return sum(self._itens.values())

    @property
    def espaco_livre(self) -> int:
        return self.capacidade - self.total

    @property
    def esta_cheio(self) -> bool:
        return self.espaco_livre == 0

    def quantidade(self, nome: str) -> int:
        return self._itens.get(nome, 0)

    def itens(self) -> dict[str, int]:
        return dict(self._itens)  # cópia: ninguém mexe no estado interno de fora

    # ---------- funcionalidade 1: adicionar item ----------
    def adicionar(self, nome: str, quantidade: int = 1) -> None:
        self._validar(nome, quantidade)
        if quantidade > self.espaco_livre:  # funcionalidade 3: capacidade máxima
            raise InventarioCheioError(
                f"sem espaço: tentou adicionar {quantidade}, livre {self.espaco_livre}"
            )
        self._itens[nome] = self.quantidade(nome) + quantidade

    # ---------- funcionalidade 2: remover item ----------
    def remover(self, nome: str, quantidade: int = 1) -> None:
        self._validar(nome, quantidade)
        if self.quantidade(nome) < quantidade:
            raise ItemInsuficienteError(
                f"'{nome}': tem {self.quantidade(nome)}, tentou remover {quantidade}"
            )
        self._itens[nome] -= quantidade
        if self._itens[nome] == 0:
            del self._itens[nome]  # não deixa "fantasma" com quantidade 0

    # ---------- funcionalidade 4: transferir itens ----------
    def transferir(self, nome: str, quantidade: int, destino: "Inventario") -> None:
        self._validar(nome, quantidade)
        if self.quantidade(nome) < quantidade:
            raise ItemInsuficienteError(f"origem não tem {quantidade}x '{nome}'")
        if quantidade > destino.espaco_livre:
            raise InventarioCheioError("destino sem espaço")
        # só mexe nos dois depois de validar tudo (operação "tudo ou nada")
        self.remover(nome, quantidade)
        destino.adicionar(nome, quantidade)

    @staticmethod
    def _validar(nome: str, quantidade: int) -> None:
        if not nome or not nome.strip():
            raise ValueError("nome do item não pode ser vazio")
        if quantidade <= 0:
            raise ValueError("quantidade deve ser maior que zero")
