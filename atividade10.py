import flet as ft

def main(page: ft.Page):
    page.title = "Formulário de Contato"

    nome = ft.TextField(label="Nome")
    email = ft.TextField(label="Email")
    mensagem = ft.TextField(label="Mensagem")

    texto_confirmacao = ft.Text("")

    def enviar(e):
        texto_confirmacao.value = "Formulário enviado com sucesso!"
        page.update()

    botao = ft.ElevatedButton("Enviar", on_click=enviar)

    page.add(
        nome,
        email,
        mensagem,
        botao,
        texto_confirmacao
    )

ft.app(target=main)
