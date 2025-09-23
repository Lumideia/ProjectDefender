import pygame
from typing import Dict, List, Tuple, Optional

from src.constant.world import WORLD_BUS
from src.enteties.character_instance import Grenadier, ForceUser
from src.rules.events.types import Event, EventCtx
from src.rules.perks.index import get_additional_jedi_perks, get_additional_common_perks
from src.rules.perks.perk import Perk

# --- загрузка текстов перков ---
from src.rules.perks.description.active import ACTIVE_PERKS
from src.rules.perks.description.aura import AURA_PERKS
from src.rules.perks.description.one_time import ONE_TIME_PERKS
from src.rules.perks.description.passive import PASSIVE_PERKS
from src.ui import runtime
from src.ui.perks_screen.Sidebar import Sidebar
from src.ui.perks_screen.additional_perks_panel import AdditionalPerksPanel
from src.ui.perks_screen.character_create import CreateCharacterForm
from src.ui.perks_screen.character_stats import CharacterStatsPanel
from src.ui.perks_screen.inventory_panel import InventoryPanel
from src.ui.perks_screen.tile_grid import TileGrid
from src.ui.theme import COLORS
from src.utils.double_click import DoubleClickTracker

import src.ui.weapons_screen as shoot_helper


def _merge_titles() -> Dict[int, str]:
    d: Dict[int, str] = {}
    for src in (ONE_TIME_PERKS, PASSIVE_PERKS, ACTIVE_PERKS, AURA_PERKS):
        try:
            d.update({pid: meta["title"] for pid, meta in src.items()})
        except Exception:
            pass
    return d

def _merge_descs() -> Dict[int, str]:
    d: Dict[int, str] = {}
    for src in (ONE_TIME_PERKS, PASSIVE_PERKS, ACTIVE_PERKS, AURA_PERKS):
        try:
            d.update({pid: meta["description"] for pid, meta in src.items()})
        except Exception:
            pass
    return d

UI_TITLES: Dict[int, str] = _merge_titles()
UI_DESCS:  Dict[int, str] = _merge_descs()


# ======================================================================
#   UI-элементы
# ======================================================================


# ======================================================================
#   Основной экран
# ======================================================================

class PerkScreen:
    def __init__(self, screen: pygame.Surface, initial: Optional[Grenadier] = None):
        self.screen = screen
        sw, sh = screen.get_size()

        # --- шрифты ---
        self.font_title = pygame.font.SysFont("arial", 28, bold=True)
        self.font_cell  = pygame.font.SysFont("arial", 16)
        self.font_small = pygame.font.SysFont("arial", 16)
        self.font_cd    = pygame.font.SysFont("arial", 16, bold=True)

        # --- layout ---
        self.cell_w, self.cell_h = 210, 84
        self.margin = 12
        self.start_x, self.start_y = 260, 140
        self.sidebar = Sidebar(20, 120, 230)

        self.create_form = CreateCharacterForm(self, self.screen)
        self.form_active = False
        self.form_close_time = 0
        self.form_click_lock = 200

        self.sidebar.on_add = self.create_form.open
        self.sidebar.on_delete = self._delete_active
        self.sidebar.on_rename = lambda idx: self._start_rename()
        self.sidebar.on_select = self._activate

        self.stats_panel = CharacterStatsPanel(
            x=20,
            y=self.sidebar.y + self.sidebar.visible_rows * (self.sidebar.item_height + self.sidebar.margin) + 40,
            w=230,
            h=250
        )

        self.grid = TileGrid(260, 180, 210, 50, 12, colors=COLORS)

        self.inventory_panel = InventoryPanel(
            x=self.start_x + self.grid.w + 10,
            y=40,
            w=200
        )
        self.inventory_modal_open = False


        self.random_perks_panel = AdditionalPerksPanel(
            self, pygame.Rect(
                0,
                40,
                int(sw),
                int(sh * 0.85),
            ),
    [])
        self.random_perks_modal_open = False
        # --- цвета ---

        # --- верхние кнопки ---

        self.hovered_perk: Optional[Perk] = None
        self.renaming = False
        self.rename_text = ""
        self.rename_rect = pygame.Rect(sw//2 - 180, 80, 360, 40)

        self.dbl = DoubleClickTracker()
        self.btn_end_turn = pygame.Rect(sw - 200, sh - 60, 180, 50)
        self.btn_shoot = pygame.Rect(sw - 400, sh - 60, 180, 50)
        self.btn_rnd_perks = pygame.Rect(sw - 600, sh - 60, 180, 50)

        self.character = None
        self.active_modal: Optional[object] = None

    # ---------------- персонажи ----------------
    def _activate(self, idx: int):
        self.sidebar.set_active(idx)
        self.character, self.character_name = self.sidebar.characters[idx]
        self.grid.rebuild(self.character, self)
        self.stats_panel.set_character(self.character)
        self.inventory_panel.set_character(self.character)


    def _delete_active(self):
        if not self.sidebar.characters:
            return
        del self.sidebar.characters[self.sidebar.active_idx]
        if not self.sidebar.characters:
            pass
        else:
            self._activate(max(0, self.sidebar.active_idx - 1))
        self.grid.rebuild(self.character, self)

    def _start_rename(self):
        self.renaming = True
        self.rename_text = self.sidebar.characters[self.sidebar.active_idx][1]
        try:
            pygame.key.start_text_input()
        except Exception:
            pass

    def _commit_rename(self):
        name = self.rename_text.strip() or self.sidebar.characters[self.sidebar.active_idx][1]
        self.sidebar.characters[self.sidebar.active_idx] = (self.character, name)
        self.character_name = name
        self.renaming = False
        try:
            pygame.key.stop_text_input()
        except Exception:
            pass


    # ---------------- отрисовка ----------------
    def draw(self):
        rect = pygame.Rect(0, 40, self.screen.get_width(), self.screen.get_height())
        pygame.draw.rect(self.screen, COLORS['BG'], rect)
        self.sidebar.draw(self.screen)

        # --- новая кнопка внизу ---
        self._draw_button(self.btn_end_turn, "Конец хода")
        self._draw_button(self.btn_shoot, "Стрелять")
        if self.character:
            self._draw_button(self.btn_rnd_perks, "Ранд. навыки")

        if self.inventory_modal_open:
            self.inventory_panel.draw_modal(self.screen, self.font_small, self.character.inventory)

            # --- показываем описание выбранного в модалке ---
            if self.inventory_panel.modal_hovered_desc:
                self._draw_selected_info_text(
                    title=self.inventory_panel.modal_hovered or "",
                    desc=self.inventory_panel.modal_hovered_desc
                )
            return  # блокируем отрисовку остального


        # грид
        if self.sidebar.characters and not self.create_form.active:
            self.inventory_panel.draw(self.screen, self.font_small, self.character.inventory)
            self.stats_panel.draw(self.screen)
            self.grid.draw(self.screen)
            if self.inventory_panel.hovered_desc:
                self._draw_selected_info_text(
                    title=self.inventory_panel.hovered or "",
                    desc=self.inventory_panel.hovered_desc
                )
            elif self.grid.hovered_perk:
                self._draw_selected_info(self.grid.hovered_perk)

        if self.renaming:
            self._draw_rename_modal()

        self.create_form.draw()
        if self.character:
            self.random_perks_panel.draw(self.screen, self.character)



    def _draw_button(self, rect: pygame.Rect, text: str):
        mx, my = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mx, my)
        pygame.draw.rect(self.screen, COLORS['BTN_HL'] if hovered else COLORS['BTN'], rect, border_radius=6)
        pygame.draw.rect(self.screen, COLORS['FRAME'], rect, 1, border_radius=6)
        label = self.font_title.render(text, True, COLORS['TEXT'])
        self.screen.blit(label, label.get_rect(center=rect.center))

    def _draw_info_box(self, title: str, desc: str):
        box = pygame.Rect(
            self.start_x,
            self.start_y - 100,
            self.grid.w,
            130
        )
        pygame.draw.rect(self.screen, (18, 18, 28), box, border_radius=6)
        pygame.draw.rect(self.screen, COLORS['FRAME'], box, 1, border_radius=6)

        t1 = self.font_cell.render(title, True, COLORS['TEXT'])
        self.screen.blit(t1, (box.x + 10, box.y + 8))
        self._blit_wrapped(desc, (box.x + 10, box.y + 30),
                           box.width - 20, self.font_small, COLORS['DIM'])

    def _draw_selected_info_text(self, title: str, desc: str):
        box = pygame.Rect(
            self.start_x,
            self.start_y - 100,
            self.grid.w,
            130
        )
        pygame.draw.rect(self.screen, (18, 18, 28), box, border_radius=6)
        pygame.draw.rect(self.screen, COLORS['FRAME'], box, 1, border_radius=6)
        t1 = self.font_cell.render(title, True, COLORS['TEXT'])
        self.screen.blit(t1, (box.x + 10, box.y + 8))
        self._blit_wrapped(desc, (box.x + 10, box.y + 30), box.width - 20, self.font_small, COLORS['DIM'])


    def _draw_selected_info(self, perk: Perk):
        title = self._perk_title(perk)
        desc = UI_DESCS.get(perk.perk_id, "")
        self._draw_info_box(title, desc)

    # ---------------- события ----------------

    def handle_event(self, event: pygame.event.Event):
        # TODO: REFACTOR THIS PIECE OF ...
        if self.active_modal:
            if self.create_form.active:
                new_char = self.create_form.handle_event(event)
                if new_char:
                    self.sidebar.add_character(new_char, new_char.character.name)
                    self._activate(len(self.sidebar.characters) - 1)
                    self.grid.rebuild(self.character, self)
                    self.form_close_time = pygame.time.get_ticks()

            elif self.random_perks_panel.active:
                new_perk = self.random_perks_panel.handle_event(event, self.character)
                if new_perk:
                    self.character.add_perk(new_perk)
                    self.grid.rebuild(self.character, self)

            return

        if pygame.time.get_ticks() - self.form_close_time < self.form_click_lock:
            return

        self.sidebar.handle_event(event)

        if self.sidebar.characters:
            # сначала пробрасываем клик в панель инвентаря
            self.inventory_panel.handle_event(event, self.character.inventory,
                                              on_add=self._open_inventory_modal)

            # если открыта модалка – блокируем всё остальное
            if self.inventory_modal_open:
                if self.inventory_panel.handle_modal_event(event, self.character.inventory):
                    self.inventory_modal_open = False
                return  # <-- ВАЖНО: выходим, чтобы не обрабатывались другие элементы

            self.stats_panel.handle_event(event)

        if self.renaming:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._commit_rename()
                elif event.key == pygame.K_ESCAPE:
                    self.renaming = False
                    try:
                        pygame.key.stop_text_input()
                    except Exception:
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    self.rename_text = self.rename_text[:-1]
                else:
                    if event.unicode and event.unicode.isprintable():
                        self.rename_text += event.unicode
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.grid.handle_event(event, double_click=self.dbl.is_double_click())
            # --- кнопка конца хода ---
            if self.btn_end_turn.collidepoint(event.pos):
                self._on_end_turn()
                return

            if self.btn_shoot.collidepoint(event.pos):
                self._open_shoot_helper()
                return

            if self.btn_rnd_perks.collidepoint(event.pos):
                perks = (get_additional_jedi_perks() if isinstance(self.character, ForceUser)
                         else get_additional_common_perks())
                self.random_perks_panel.perks = list(perks)
                self.random_perks_panel.open()
                return
        else:
            self.grid.handle_event(event, double_click=False)


    # ---------------- утилиты ----------------
    def _open_shoot_helper(self):
        weapons = []
        if self.character.main_weapon:
            weapons.append(self.character.main_weapon)
        if getattr(self.character, "side_weapon", None):
            weapons.append(self.character.side_weapon)
        shoot_helper.custom_weapons = weapons
        shoot_helper.selected_weapon_index = 0  # сбросить выбор
        runtime.current_screen = shoot_helper  # переключение экрана

    def _open_inventory_modal(self):
        """Открывает модальное окно выбора предмета."""
        self.inventory_modal_open = True


    def _perk_title(self, perk: Perk) -> str:
        return UI_TITLES.get(perk.perk_id, perk.__class__.__name__)

    def _on_end_turn(self):
        """Вызывается при клике на кнопку 'Конец хода'."""
        # 1. триггерим глобальный ивент конца хода (если используете EventBus)
        try:
            WORLD_BUS.broadcast(Event.TURN_END, EventCtx(Event.TURN_END))
        except Exception:
            # если пока нет реализации EventBus.emit, просто пропустите
            pass

    def _blit_wrapped_center(self, text: str, rect: pygame.Rect, font: pygame.font.Font):
        lines = self._wrap_text(text, font, rect.width - 12)
        total_h = len(lines) * font.get_height()
        y = rect.y + (rect.height - total_h)//2
        for ln in lines:
            surf = font.render(ln, True, COLORS['TEXT'])
            self.screen.blit(surf, surf.get_rect(centerx=rect.centerx, y=y))
            y += font.get_height()

    def _blit_wrapped(self, text: str, pos: Tuple[int,int], max_w: int, font, color):
        x, y = pos
        for ln in self._wrap_text(text, font, max_w):
            self.screen.blit(font.render(ln, True, color), (x, y))
            y += font.get_height()

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        words = text.split()
        lines: List[str] = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if font.size(test)[0] <= max_width:
                cur = test
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        return lines

    def _draw_rename_modal(self):
        shade = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        shade.fill((0,0,0,160))
        self.screen.blit(shade, (0,0))
        pygame.draw.rect(self.screen, (30,30,40), self.rename_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLORS['FRAME'], self.rename_rect, 1, border_radius=8)
        hint = self.font_small.render("Введите имя и нажмите Enter (Esc — отмена)", True, COLORS['DIM'])
        self.screen.blit(hint, (self.rename_rect.x, self.rename_rect.y - 24))
        txt = self.font_cell.render(self.rename_text, True, COLORS['TEXT'])
        self.screen.blit(txt, (self.rename_rect.x + 10, self.rename_rect.y + 10))
        cx = self.rename_rect.x + 10 + txt.get_width() + 2
        cy = self.rename_rect.y + 10
        pygame.draw.line(self.screen, COLORS['TEXT'], (cx, cy), (cx, cy + txt.get_height()), 1)
