import flet as ft

class Pessoa:
    def __init__(self, nome, telefone, email):
        self.__nome = nome
        self.__telefone = telefone
        self.__email = email

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        if nome.strip() != "":
            self.__nome = nome

    def get_telefone(self):
        return self.__telefone

    def set_telefone(self, telefone):
        if telefone.strip() != "":
            self.__telefone = telefone

    def get_email(self):
        return self.__email

    def set_email(self, email):
        if "@" in email and email.strip() != "":
            self.__email = email

    def exibir_informacoes(self):
        return f"Nome: {self.get_nome()} | Tel: {self.get_telefone()} | Email: {self.get_email()}"


class Cliente(Pessoa):
    _contador_id = 1

    def __init__(self, nome, telefone, email):
        super().__init__(nome, telefone, email)
        self.__id = Cliente._contador_id
        Cliente._contador_id += 1

    def get_id(self):
        return self.__id

    def exibir_informacoes(self):
        return f"ID: {self.get_id()} | " + super().exibir_informacoes()


class Quarto:
    def __init__(self, numero, tipo, preco_diaria):
        self.__numero = numero
        self.__tipo = tipo
        self.__preco_diaria = preco_diaria
        self.__disponivel = True

    def get_numero(self):
        return self.__numero

    def get_tipo(self):
        return self.__tipo

    def get_preco_diaria(self):
        return self.__preco_diaria

    def esta_disponivel(self):
        return self.__disponivel

    def set_disponivel(self, valor):
        self.__disponivel = bool(valor)

    def __str__(self):
        status = "Disponível" if self.esta_disponivel() else "Ocupado"
        return f"Quarto {self.get_numero()} ({self.get_tipo()}) - R$ {self.get_preco_diaria():.2f} - {status}"


class Reserva:
    def __init__(self, dono, quarto, checkin, checkout):
        self.__dono = dono
        self.__quarto = quarto
        self.__checkin = checkin
        self.__checkout = checkout
        self.__status = "ATIVA"

    def get_dono(self):
        return self.__dono

    def get_quarto(self):
        return self.__quarto

    def get_checkin(self):
        return self.__checkin

    def set_checkin(self, v):
        self.__checkin = v

    def get_checkout(self):
        return self.__checkout

    def set_checkout(self, v):
        self.__checkout = v

    def get_status(self):
        return self.__status

    def cancelar(self):
        self.__status = "CANCELADA"


class GerenciadorDeReservas:
    def __init__(self):
        self.__clientes = []
        self.__quartos = []
        self.__reservas = []

    def listar_clientes(self):
        return self.__clientes

    def adicionar_cliente(self, cliente):
        self.__clientes.append(cliente)

    def listar_quartos(self):
        return self.__quartos

    def adicionar_quarto(self, quarto):
        self.__quartos.append(quarto)

    def quartos_disponiveis(self):
        livres = []
        for q in self.__quartos:
            if q.esta_disponivel():
                livres.append(q)
        return livres

    def listar_reservas(self):
        return self.__reservas

    def criar_reserva(self, cliente, quarto, checkin, checkout):
        if not quarto.esta_disponivel():
            return None

        reserva = Reserva(cliente, quarto, checkin, checkout)
        self.__reservas.append(reserva)
        quarto.set_disponivel(False)
        return reserva

    def cancelar_reserva(self, reserva):
        if reserva.get_status() == "ATIVA":
            reserva.cancelar()
            reserva.get_quarto().set_disponivel(True)

    def modificar_reserva(self, reserva, novo_checkin, novo_checkout):
        if reserva.get_status() != "ATIVA":
            return False
        reserva.set_checkin(novo_checkin)
        reserva.set_checkout(novo_checkout)
        return True

def main(page: ft.Page):
    page.title = "Refúgio dos Sonhos - Reservas"
    page.scroll = "auto"

    ger = GerenciadorDeReservas()

    ger.adicionar_quarto(Quarto(101, "single", 180.0))
    ger.adicionar_quarto(Quarto(102, "double", 250.0))
    ger.adicionar_quarto(Quarto(201, "suite", 450.0))

    ger.adicionar_cliente(Cliente("Maria", "1199999-1111", "maria@email.com"))
    ger.adicionar_cliente(Cliente("João", "1198888-2222", "joao@email.com"))

    msg = ft.Text("")

    lista_quartos = ft.Column()
    lista_reservas = ft.Column()
    lista_clientes = ft.Column()

    def atualizar_quartos():
        lista_quartos.controls.clear()
        for q in ger.listar_quartos():
            lista_quartos.controls.append(ft.Text(str(q)))
        page.update()

    def atualizar_reservas():
        lista_reservas.controls.clear()

        if len(ger.listar_reservas()) == 0:
            lista_reservas.controls.append(ft.Text("Nenhuma reserva cadastrada."))
            page.update()
            return

        for r in ger.listar_reservas():
            texto = (
                f"{r.get_status()} | Cliente: {r.get_dono().get_nome()} (ID {r.get_dono().get_id()}) "
                f"| Quarto: {r.get_quarto().get_numero()} | {r.get_checkin()} -> {r.get_checkout()}"
            )

            def cancelar_factory(reserva):
                def cancelar(e):
                    ger.cancelar_reserva(reserva)
                    msg.value = "Reserva cancelada!"
                    atualizar_quartos()
                    atualizar_reservas()
                return cancelar

            def modificar_factory(reserva):
                def abrir_mod(e):
                    chk_in_edit.value = reserva.get_checkin()
                    chk_out_edit.value = reserva.get_checkout()
                    dialog_modificar.data = reserva
                    dialog_modificar.open = True
                    page.update()
                return abrir_mod

            btn_cancelar = ft.ElevatedButton(
                "Cancelar",
                on_click=cancelar_factory(r),
                disabled=(r.get_status() != "ATIVA")
            )

            btn_modificar = ft.ElevatedButton(
                "Modificar",
                on_click=modificar_factory(r),
                disabled=(r.get_status() != "ATIVA")
            )

            lista_reservas.controls.append(
                ft.Row(
                    [ft.Text(texto), btn_modificar, btn_cancelar],
                    alignment="spaceBetween"
                )
            )

        page.update()

    def atualizar_clientes():
        lista_clientes.controls.clear()

        for c in ger.listar_clientes():
            def editar_factory(cliente):
                def abrir_edicao(e):
                    nome_edit.value = cliente.get_nome()
                    tel_edit.value = cliente.get_telefone()
                    email_edit.value = cliente.get_email()
                    dialog_editar_cliente.data = cliente
                    dialog_editar_cliente.open = True
                    page.update()
                return abrir_edicao

            linha = ft.Row(
                [
                    ft.Text(cliente.exibir_informacoes() if (cliente := c) else ""),
                    ft.ElevatedButton("Editar", on_click=editar_factory(c))
                ],
                alignment="spaceBetween"
            )
            lista_clientes.controls.append(linha)

        page.update()

    nome_c = ft.TextField(label="Nome")
    tel_c = ft.TextField(label="Telefone")
    email_c = ft.TextField(label="Email")

    def add_cliente(e):
        c = Cliente(nome_c.value, tel_c.value, email_c.value)
        ger.adicionar_cliente(c)

        nome_c.value = ""
        tel_c.value = ""
        email_c.value = ""

        msg.value = "Cliente adicionado!"
        atualizar_clientes()
        page.update()

    nome_edit = ft.TextField(label="Nome")
    tel_edit = ft.TextField(label="Telefone")
    email_edit = ft.TextField(label="Email")

    def salvar_edicao_cliente(e):
        cliente = dialog_editar_cliente.data
        cliente.set_nome(nome_edit.value)
        cliente.set_telefone(tel_edit.value)
        cliente.set_email(email_edit.value)

        dialog_editar_cliente.open = False
        msg.value = "Cliente editado!"
        atualizar_clientes()
        page.update()

    dialog_editar_cliente = ft.AlertDialog(
        title=ft.Text("Editar cliente"),
        content=ft.Column([nome_edit, tel_edit, email_edit], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog_editar_cliente, "open", False) or page.update()),
            ft.ElevatedButton("Salvar", on_click=salvar_edicao_cliente),
        ],
    )

    dd_cliente = ft.Dropdown(label="Cliente")
    dd_quarto = ft.Dropdown(label="Quarto disponível")
    checkin = ft.TextField(label="Check-in (ex: 10/10/2026)")
    checkout = ft.TextField(label="Check-out (ex: 12/10/2026)")

    def carregar_dropdowns():
        dd_cliente.options = []
        for c in ger.listar_clientes():
            dd_cliente.options.append(
                ft.dropdown.Option(str(c.get_id()), f"{c.get_nome()} (ID {c.get_id()})")
            )

        dd_quarto.options = []
        for q in ger.quartos_disponiveis():
            dd_quarto.options.append(
                ft.dropdown.Option(str(q.get_numero()), f"{q.get_numero()} - {q.get_tipo()}")
            )

    def abrir_dialogo_reserva(e):
        carregar_dropdowns()
        dialog_reserva.open = True
        page.update()

    def confirmar_reserva(e):
        cliente_escolhido = None
        for c in ger.listar_clientes():
            if str(c.get_id()) == dd_cliente.value:
                cliente_escolhido = c

        quarto_escolhido = None
        for q in ger.listar_quartos():
            if str(q.get_numero()) == dd_quarto.value:
                quarto_escolhido = q

        if cliente_escolhido is None or quarto_escolhido is None:
            msg.value = "Selecione cliente e quarto."
        else:
            r = ger.criar_reserva(cliente_escolhido, quarto_escolhido, checkin.value, checkout.value)
            if r is None:
                msg.value = "Quarto indisponível."
            else:
                msg.value = "Reserva criada!"
                atualizar_quartos()
                atualizar_reservas()

        dialog_reserva.open = False
        page.update()

    dialog_reserva = ft.AlertDialog(
        title=ft.Text("Nova Reserva"),
        content=ft.Column([dd_cliente, dd_quarto, checkin, checkout], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog_reserva, "open", False) or page.update()),
            ft.ElevatedButton("Confirmar", on_click=confirmar_reserva),
        ],
    )

    chk_in_edit = ft.TextField(label="Novo check-in")
    chk_out_edit = ft.TextField(label="Novo check-out")

    def salvar_modificacao_reserva(e):
        reserva = dialog_modificar.data
        ok = ger.modificar_reserva(reserva, chk_in_edit.value, chk_out_edit.value)
        if ok:
            msg.value = "Reserva modificada!"
        else:
            msg.value = "Não foi possível modificar."

        dialog_modificar.open = False
        atualizar_reservas()
        page.update()

    dialog_modificar = ft.AlertDialog(
        title=ft.Text("Modificar reserva"),
        content=ft.Column([chk_in_edit, chk_out_edit], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog_modificar, "open", False) or page.update()),
            ft.ElevatedButton("Salvar", on_click=salvar_modificacao_reserva),
        ],
    )

    tela_quartos = ft.Column(
        [
            ft.Text("Tela inicial: Quartos e disponibilidade"),
            ft.ElevatedButton("Fazer reserva", on_click=abrir_dialogo_reserva),
            ft.Divider(),
            lista_quartos,
        ]
    )

    tela_reservas = ft.Column(
        [
            ft.Text("Tela de visualização de reservas (cancelar/modificar)"),
            ft.Divider(),
            lista_reservas,
        ]
    )

    tela_clientes = ft.Column(
        [
            ft.Text("Gerenciamento de clientes (visualizar/adicionar/editar)"),
            nome_c,
            tel_c,
            email_c,
            ft.ElevatedButton("Adicionar cliente", on_click=add_cliente),
            ft.Divider(),
            lista_clientes,
        ]
    )

    page.overlay.append(dialog_reserva)
    page.overlay.append(dialog_editar_cliente)
    page.overlay.append(dialog_modificar)

    page.add(
        tela_quartos,
        ft.Divider(),
        tela_reservas,
        ft.Divider(),
        tela_clientes,
        ft.Divider(),
        msg
    )

    atualizar_quartos()
    atualizar_reservas()
    atualizar_clientes()


ft.app(target=main)