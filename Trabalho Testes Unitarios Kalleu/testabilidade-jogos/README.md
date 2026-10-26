# Testabilidade em Jogos — Inventário com testes unitários e de integração

Sistema de **inventário** de jogo (adicionar, remover, capacidade máxima, transferir) com a lógica
isolada da engine usando **MVP** (Model–View–Presenter). Testado com **pytest** (Python 3.10+).

## Rodar
```bash
pip install -r requirements.txt
pytest -v                # roda os 24 testes
python src/main.py       # demo no terminal (a View é só print)
```

## Estrutura
```
src/inventario/inventario.py   MODEL      lógica pura (zero dependência de engine)
src/inventario/presenter.py    PRESENTER  liga Model e View
src/inventario/excecoes.py     exceções de regra de negócio
src/main.py                    View de console (demo)
tests/test_inventario.py       testes UNITÁRIOS do Model (padrão AAA + edge cases)
tests/test_presenter.py        teste de INTEGRAÇÃO (Presenter + Model + FakeView)
pytest.ini                     configuração (pythonpath = src)
```

## Funcionalidades testadas
1. **Adicionar item** (empilha repetidos, rejeita qtd <= 0 e nome vazio)
2. **Remover item** (parcial, total sem "item fantasma", inexistente, acima do que tem)
3. **Capacidade máxima** (limite exato, limite + 1, capacidade inválida)
4. **Transferir itens** (entre inventários, operação "tudo ou nada")

## Demo de falha (para a apresentação)
Em `inventario.py`, troque `if quantidade > self.espaco_livre` por `>=` e rode `pytest`:
3 testes quebram, mostrando que os edge cases pegam o bug. Desfaça e volte a ficar tudo verde.

## Enviar para o Git
```bash
git init -b main
git add -A
git commit -m "Inventário com testes unitários e de integração"
git remote add origin <URL-DO-REPO>
git push -u origin main
```
