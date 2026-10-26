"""Testes unitários do Model (Inventario). Padrão AAA: Arrange / Act / Assert."""
import pytest

from inventario import Inventario, InventarioCheioError, ItemInsuficienteError


@pytest.fixture
def inv():
    return Inventario(capacidade=10)


# ============ 1. ADICIONAR ============
class TestAdicionar:
    def test_adiciona_item_novo(self, inv):
        # Arrange: inventário vazio (fixture)
        # Act
        inv.adicionar("Poção", 3)
        # Assert
        assert inv.quantidade("Poção") == 3
        assert inv.espaco_livre == 7

    def test_empilha_item_repetido(self, inv):
        inv.adicionar("Poção", 2)
        inv.adicionar("Poção", 3)
        assert inv.quantidade("Poção") == 5

    @pytest.mark.parametrize("qtd", [0, -1, -100])  # edge case: zero e negativos
    def test_quantidade_invalida_levanta_erro(self, inv, qtd):
        with pytest.raises(ValueError):
            inv.adicionar("Poção", qtd)

    @pytest.mark.parametrize("nome", ["", "   "])  # edge case: nome vazio
    def test_nome_vazio_levanta_erro(self, inv, nome):
        with pytest.raises(ValueError):
            inv.adicionar(nome)


# ============ 2. REMOVER ============
class TestRemover:
    def test_remove_quantidade_parcial(self, inv):
        inv.adicionar("Poção", 5)
        inv.remover("Poção", 2)
        assert inv.quantidade("Poção") == 3

    def test_remover_tudo_apaga_a_entrada(self, inv):
        inv.adicionar("Espada")
        inv.remover("Espada")
        assert "Espada" not in inv.itens()  # sem item "fantasma" com 0

    def test_remover_item_inexistente_levanta_erro(self, inv):
        with pytest.raises(ItemInsuficienteError):
            inv.remover("Arco")

    def test_remover_mais_do_que_tem_nao_altera_estado(self, inv):
        inv.adicionar("Poção", 2)
        with pytest.raises(ItemInsuficienteError):
            inv.remover("Poção", 5)
        assert inv.quantidade("Poção") == 2  # estado intacto


# ============ 3. CAPACIDADE MÁXIMA ============
class TestCapacidade:
    def test_inventario_cheio_nao_aceita_mais(self):
        inv = Inventario(capacidade=2)
        inv.adicionar("Poção", 2)
        assert inv.esta_cheio
        with pytest.raises(InventarioCheioError):
            inv.adicionar("Espada")

    def test_enche_exatamente_no_limite(self):  # edge case: limite exato
        inv = Inventario(capacidade=3)
        inv.adicionar("Poção", 3)
        assert inv.espaco_livre == 0

    def test_um_acima_do_limite_falha(self):  # edge case: limite + 1
        inv = Inventario(capacidade=3)
        with pytest.raises(InventarioCheioError):
            inv.adicionar("Poção", 4)
        assert inv.total == 0

    @pytest.mark.parametrize("cap", [0, -5])
    def test_capacidade_invalida(self, cap):
        with pytest.raises(ValueError):
            Inventario(capacidade=cap)


# ============ 4. TRANSFERIR ============
class TestTransferir:
    def test_transfere_entre_inventarios(self):
        origem, destino = Inventario(10), Inventario(10)
        origem.adicionar("Poção", 5)
        origem.transferir("Poção", 2, destino)
        assert origem.quantidade("Poção") == 3
        assert destino.quantidade("Poção") == 2

    def test_destino_cheio_nao_perde_item_da_origem(self):  # tudo ou nada
        # Arrange: origem com 5 poções, destino com capacidade 1
        origem, destino = Inventario(10), Inventario(1)
        origem.adicionar("Poção", 5)
        # Act: tenta transferir 2 (não cabe) -> deve falhar
        with pytest.raises(InventarioCheioError):
            origem.transferir("Poção", 2, destino)
        # Assert: nada foi perdido nem duplicado
        assert origem.quantidade("Poção") == 5
        assert destino.total == 0

    def test_origem_sem_item_levanta_erro(self):
        origem, destino = Inventario(10), Inventario(10)
        with pytest.raises(ItemInsuficienteError):
            origem.transferir("Poção", 1, destino)
        assert destino.total == 0


# ============ encapsulamento ============
def test_itens_devolve_copia(inv):
    inv.adicionar("Poção", 1)
    inv.itens()["Poção"] = 999  # tentando "hackear" por fora
    assert inv.quantidade("Poção") == 1
