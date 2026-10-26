class InventarioCheioError(Exception):
    """Lançada quando não há espaço livre suficiente no inventário."""


class ItemInsuficienteError(Exception):
    """Lançada quando o item não existe (ou não há quantidade suficiente)."""
