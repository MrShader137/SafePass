import flet as ft
from ui import build_ui

def main(page: ft.Page):
    build_ui(page) # Ele vai configurar a página e abrir a main screen

ft.app(target=main)