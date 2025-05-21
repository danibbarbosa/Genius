import flet as ft
import random
import asyncio

COLORS = ["red", "green", "blue", "yellow"]

class Genius:
    def __init__(self, page: ft.Page):
        self.page = page
        self.sequence = []
        self.user_sequence = []
        self.score = 0
        self.buttons = {}
        self.status_text = ft.Text(value="Aperte Start! para Começar", size=20)
        self.score_text = ft.Text(value="Pontos: 0", size=16)

        self.start_button = ft.ElevatedButton("Start!", on_click=self.start_game)
        self.page.add(self.status_text, self.score_text)

        self.create_buttons()
        self.page.add(self.start_button)

    def create_buttons(self):
        for color in COLORS:
            async def on_color_click(e, c=color):
                await self.user_click(c)

            btn = ft.Container(
                content=ft.Text(""),
                bgcolor=color,
                width=100,
                height=100,
                border_radius=10
            )
            btn.on_click = lambda e, c=color: asyncio.run(self.user_click(c))

            self.buttons[color] = btn

        self.page.add(ft.Row([self.buttons[c] for c in COLORS], alignment="center"))

    async def flash_button(self, color):
        self.buttons[color].bgcolor = "white"
        self.page.update()
        await asyncio.sleep(0.5) #tempo, em segundos, em que o botão aparece branco
        self.buttons[color].bgcolor = color
        self.page.update()
        await asyncio.sleep(0.5) #tempo, em segundos, em que a cor do botão aparece

    async def play_sequence(self):
        for color in self.sequence:
            await self.flash_button(color)
            await asyncio.sleep(0.6) #tempo, em segundos, para a troca do botão

    async def start_game(self, e=None):
        self.sequence = []
        self.user_sequence = []
        self.score = 0
        self.score_text.value = "Pontos: 0"
        self.status_text.value = "Preste Atenção na Sequência!"
        self.page.update()
        await asyncio.sleep(0.5) #tempo, em segundos, para começar o jogo
        await self.next_round()

    async def next_round(self):
        self.user_sequence = []
        next_color = random.choice(COLORS)
        self.sequence.append(next_color)
        self.status_text.value = f"Fase:  {len(self.sequence)}"
        self.page.update()
        await asyncio.sleep(1.2) #pausa para começar a próxima fase
        await self.play_sequence()

    async def user_click(self, color):
        self.user_sequence.append(color)
        idx = len(self.user_sequence) - 1

        if self.user_sequence[idx] != self.sequence[idx]:
            self.status_text.value = "Game Over!"
            self.page.update()
            return

        if len(self.user_sequence) == len(self.sequence):
            self.score += 1
            self.score_text.value = f"Pontos:  {self.score}"
            self.page.update()
            await self.next_round()

async def main(page: ft.Page):
    page.title = "Genius!!!"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    Genius(page)

ft.app(target=main)




