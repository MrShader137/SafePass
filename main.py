import flet as ft
from ui import build_ui

def main(page: ft.Page):
    build_ui(page)

ft.app(target=main)
