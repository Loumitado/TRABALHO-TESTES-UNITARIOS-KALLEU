"""PRESENTER: faz a ponte entre Model e View. A View é qualquer objeto com os 2 métodos abaixo
(na Unity seria um MonoBehaviour; no Godot, um Node; nos testes, um FakeView)."""
from .excecoes import InventarioCheioError, ItemInsuficienteError


class InventarioPresenter:
    def __init__(self, inventario, view):
        self.inventario = inventario
        self.view = view

    def coletar(self, nome: str, quantidade: int = 1) -> None:
        try:
            self.inventario.adicionar(nome, quantidade)
            self.view.mostrar_mensagem(f"Coletou {quantidade}x {nome}")
        except InventarioCheioError:
            self.view.mostrar_mensagem("Mochila cheia!")
        except ValueError as e:
            self.view.mostrar_mensagem(f"Ação inválida: {e}")
        self._atualizar()

    def descartar(self, nome: str, quantidade: int = 1) -> None:
        try:
            self.inventario.remover(nome, quantidade)
            self.view.mostrar_mensagem(f"Descartou {quantidade}x {nome}")
        except ItemInsuficienteError:
            self.view.mostrar_mensagem(f"Você não tem {nome} suficiente")
        except ValueError as e:
            self.view.mostrar_mensagem(f"Ação inválida: {e}")
        self._atualizar()

    def _atualizar(self) -> None:
        self.view.mostrar_inventario(self.inventario.itens(), self.inventario.espaco_livre)
