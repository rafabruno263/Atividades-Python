import flet as ft

def main(page: ft.Page):
    page.title = "Lista de Tarefas"

    tarefas_coluna = ft.Column()

    input_tarefa = ft.TextField(label="Digite a tarefa")

    def adicionar_tarefa(e):
        texto = input_tarefa.value.strip()
        if texto != "":
            tarefas_coluna.controls.append(ft.Text(texto))
            input_tarefa.value = ""
            page.update()

    btn_add = ft.ElevatedButton("Adicionar", on_click=adicionar_tarefa)

    page.add(
        input_tarefa,
        btn_add,
        ft.Text("Tarefas:"),
        tarefas_coluna
    )

ft.app(target=main)
