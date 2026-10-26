"""Demo no terminal: a View aqui é só print(). Troque por Unity/Godot e a lógica não muda."""
from inventario import Inventario, InventarioPresenter


class ViewConsole:
    def mostrar_mensagem(self, texto):
        print(f"> {texto}")

    def mostrar_inventario(self, itens, livre):
        print(f"  Itens: {itens} | espaço livre: {livre}")


if __name__ == "__main__":
    p = InventarioPresenter(Inventario(capacidade=5), ViewConsole())
    p.coletar("Poção", 3)
    p.coletar("Espada")
    p.coletar("Escudo", 2)   # não cabe
    p.descartar("Poção", 1)
    p.descartar("Arco")      # não tem
