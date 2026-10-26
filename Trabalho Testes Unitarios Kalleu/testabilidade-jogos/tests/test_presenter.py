"""Teste de INTEGRAÇÃO: Presenter + Model reais, View falsa (FakeView) no lugar da tela/engine."""
from inventario import Inventario, InventarioPresenter


class FakeView:
    """Grava o que o Presenter mandou mostrar. Dá pra testar UI sem abrir a engine."""

    def __init__(self):
        self.mensagens = []
        self.ultimo_estado = None

    def mostrar_mensagem(self, texto):
        self.mensagens.append(texto)

    def mostrar_inventario(self, itens, livre):
        self.ultimo_estado = (itens, livre)


def test_coletar_atualiza_model_e_view():
    view = FakeView()
    p = InventarioPresenter(Inventario(5), view)
    p.coletar("Poção", 2)
    assert view.mensagens[-1] == "Coletou 2x Poção"
    assert view.ultimo_estado == ({"Poção": 2}, 3)


def test_coletar_com_mochila_cheia_avisa_o_jogador():
    view = FakeView()
    p = InventarioPresenter(Inventario(1), view)
    p.coletar("Espada")
    p.coletar("Escudo")
    assert view.mensagens[-1] == "Mochila cheia!"
    assert view.ultimo_estado == ({"Espada": 1}, 0)


def test_descartar_item_que_nao_tem_avisa_o_jogador():
    view = FakeView()
    p = InventarioPresenter(Inventario(5), view)
    p.descartar("Arco")
    assert "não tem" in view.mensagens[-1]


def test_quantidade_negativa_vira_mensagem_e_nao_excecao():
    view = FakeView()
    p = InventarioPresenter(Inventario(5), view)
    p.coletar("Poção", -3)  # não pode estourar o jogo
    assert view.mensagens[-1].startswith("Ação inválida")
