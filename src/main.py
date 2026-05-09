"""Entrypoint do gallery — configura page e renderiza GalleryApp.

Toda a lógica visual e de roteamento vive em `gallery/app.py`. Este
arquivo só configura janela, logger e dispara `page.render(GalleryApp)`.
"""

from pathlib import Path

import flet as ft
from loguru import logger

from gallery.app import GalleryApp

LOG_PATH = Path("storage/data/app.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logger.add(str(LOG_PATH), rotation="1 MB", retention=3)


async def main(page: ft.Page) -> None:
    page.title = "flet-wizards — gallery"
    page.padding = 0
    page.bgcolor = "#050508"
    page.window.width = 1280
    page.window.height = 820
    page.render(GalleryApp)


ft.run(main)
