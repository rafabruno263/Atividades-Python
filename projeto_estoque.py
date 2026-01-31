import sqlite3
from datetime import datetime

class Produto:
    def __init__(self, id, nome, descricao, quantidade, preco):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = preco


class Venda:
    def __init__(self, id_venda, id_produto, quantidade, data_venda):
        self.id_venda = id_venda
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.data_venda = data_venda

class EstoqueDB:
    def __init__(self, caminho_db="estoque.db"):
        self.conn = sqlite3.connect(caminho_db)
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER NOT NULL,
            quantidade_vendida INTEGER NOT NULL,
            data_venda TEXT NOT NULL,
            FOREIGN KEY (id_produto) REFERENCES produtos(id)
        )
        """)

        self.conn.commit()

    def cadastrar_produto(self, nome, descricao, quantidade, preco):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, descricao, quantidade, preco) VALUES (?, ?, ?, ?)",
            (nome, descricao, quantidade, preco)
        )
        self.conn.commit()

    def listar_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome, descricao, quantidade, preco FROM produtos ORDER BY id")
        return cursor.fetchall()

    def buscar_produto_por_id(self, id_produto):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome, descricao, quantidade, preco FROM produtos WHERE id = ?", (id_produto,))
        return cursor.fetchone()

    def atualizar_quantidade(self, id_produto, nova_quantidade):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, id_produto))
        self.conn.commit()

    def remover_produto(self, id_produto):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM vendas WHERE id_produto = ?", (id_produto,))
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        self.conn.commit()

    def registrar_venda(self, id_produto, quantidade_vendida):
        produto = self.buscar_produto_por_id(id_produto)
        if not produto:
            return False, "Produto não encontrado."

        quantidade_atual = produto[3]
        if quantidade_vendida <= 0:
            return False, "Quantidade vendida deve ser maior que 0."
        if quantidade_vendida > quantidade_atual:
            return False, "Estoque insuficiente."

        nova_quantidade = quantidade_atual - quantidade_vendida
        self.atualizar_quantidade(id_produto, nova_quantidade)

        data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO vendas (id_produto, quantidade_vendida, data_venda) VALUES (?, ?, ?)",
            (id_produto, quantidade_vendida, data_venda)
        )
        self.conn.commit()
        return True, "Venda registrada com sucesso!"

    def listar_vendas(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT v.id_venda, v.id_produto, p.nome, v.quantidade_vendida, v.data_venda
            FROM vendas v
            JOIN produtos p ON p.id = v.id_produto
            ORDER BY v.id_venda
        """)
        return cursor.fetchall()

    def fechar(self):
        self.conn.close()

def ler_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_float(msg):
    while True:
        try:
            return float(input(msg).replace(",", "."))
        except ValueError:
            print("Digite um número válido (ex: 10.50).")


def main():
    db = EstoqueDB()

    while True:
        print("\n==== SISTEMA DE ESTOQUE (CRUD) ====")
        print("1) Cadastrar produto (Create)")
        print("2) Listar produtos (Read)")
        print("3) Atualizar quantidade (Update)")
        print("4) Remover produto (Delete)")
        print("5) Registrar venda")
        print("6) Listar vendas")
        print("0) Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome = input("Nome do produto: ").strip()
            descricao = input("Descrição: ").strip()
            quantidade = ler_int("Quantidade disponível: ")
            preco = ler_float("Preço: ")

            if nome == "":
                print("Nome não pode ser vazio.")
            elif quantidade < 0:
                print("Quantidade não pode ser negativa.")
            elif preco < 0:
                print("Preço não pode ser negativo.")
            else:
                db.cadastrar_produto(nome, descricao, quantidade, preco)
                print("Produto cadastrado!")

        elif opcao == "2":
            produtos = db.listar_produtos()
            if not produtos:
                print("Nenhum produto cadastrado.")
            else:
                print("\n--- PRODUTOS ---")
                for (idp, nome, desc, qtd, preco) in produtos:
                    print(f"ID: {idp} | {nome} | Qtd: {qtd} | R$ {preco:.2f} | {desc}")

        elif opcao == "3":
            id_prod = ler_int("ID do produto: ")
            produto = db.buscar_produto_por_id(id_prod)
            if not produto:
                print("Produto não encontrado.")
            else:
                nova_qtd = ler_int("Nova quantidade: ")
                if nova_qtd < 0:
                    print("Quantidade não pode ser negativa.")
                else:
                    db.atualizar_quantidade(id_prod, nova_qtd)
                    print("Quantidade atualizada!")

        elif opcao == "4":
            id_prod = ler_int("ID do produto para remover: ")
            produto = db.buscar_produto_por_id(id_prod)
            if not produto:
                print("Produto não encontrado.")
            else:
                db.remover_produto(id_prod)
                print("Produto removido!")

        elif opcao == "5":
            id_prod = ler_int("ID do produto vendido: ")
            qtd_vendida = ler_int("Quantidade vendida: ")
            ok, msg = db.registrar_venda(id_prod, qtd_vendida)
            print(msg)


        elif opcao == "6":
            vendas = db.listar_vendas()
            if not vendas:
                print("Nenhuma venda registrada.")
            else:
                print("\n--- VENDAS ---")
                for (idv, idp, nome_prod, qtd, data) in vendas:
                    print(f"Venda {idv} | Produto {idp} ({nome_prod}) | Qtd: {qtd} | Data: {data}")

        elif opcao == "0":
            db.fechar()
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()