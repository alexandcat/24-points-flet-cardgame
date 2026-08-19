"""
twentyfour_card_render.py
24 Points card face renderer with Flet
Render standard playing card pip layout(A - 10), corner markers, suit symbols.
Reference: 52CardEngine card layout
Run: python twentyfour_card_render.py
"""
import math
import random
import re
import itertools
import flet as ft

# Color scheme
CARD_WHITE = "#F2F2F2"    # Card background (242, 242, 242)
CARD_BORDER = "#D3D3D3"   # Card border (211, 211, 211)
CARD_RED = "#C72C48"      # Hearts/Diamonds (199, 44, 72)
CARD_BLACK = "#1C1C1E"    # Spades/Clubs (28, 28, 30)
SUITS = ["♠", "♥", "♦", "♣"]
CARD_W, CARD_H = 90, 126  # Card dimensions
CARD_BORDER_THICK = 2     # Card border thickness

# 3‑column × 7‑row array: suit positions for each rank (rows 1‑7, columns 1‑3)
# Rank 1 is placed at the center (4,2); Rank 2 at row 1 column 2 and row 7 column 2;
# Remaining positions are arranged by symmetric recursion. The number of suits matches the rank value.
PIP_POSITIONS = {
    1: [(4, 2)],
    2: [(1, 2), (7, 2)],
    3: [(1, 2), (4, 2), (7, 2)],
    4: [(1, 1), (1, 3), (7, 1), (7, 3)],
    5: [(1, 1), (1, 3), (4, 2), (7, 1), (7, 3)],
    6: [(1, 1), (1, 3), (4, 1), (4, 3), (7, 1), (7, 3)],
    7: [(1, 1), (1, 3), (4, 1), (4, 3), (7, 1), (7, 3), (2, 2)],
    8: [(1, 1), (4, 1), (1, 3), (4, 3), (7, 1), (7, 3), (2, 2), (6, 2)],
    9: [(1, 1), (1, 3), (3, 1), (3, 3), (4, 2), (5, 1), (5, 3), (7, 1), (7, 3)],
    10: [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3), (5, 1), (5, 3), (6, 2), (7, 1), (7, 3)],
}


def rank_label(rank: int) -> str:
    """ Map rank 1 to A. """
    return "A" if rank == 1 else str(rank)


def suit_color(suit: str) -> str:
    """ Map hearts and diamonds to red, spades and clubs to black. """
    return CARD_RED if suit in ("♥", "♦") else CARD_BLACK


def make_corner(label: str, suit: str, color: str) -> ft.Column:
    """ Corner marker: rank + suit, arranged vertically. """
    return ft.Column(
        controls=[
            ft.Text(
                label, size=15, weight=ft.FontWeight.BOLD, color=color,
                style=ft.TextStyle(height=0.9),
                scale=ft.Scale(scale_x=0.75, alignment=ft.Alignment.CENTER_LEFT)
                if label == "10" else None,
            ),
            ft.Text(suit, size=10, color=color, style=ft.TextStyle(height=0.9)),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def make_pip_grid(suit: str, color: str, rank: int,
                  box_w: float, box_h: float) -> ft.Stack:
    """ Overlay mode: one full-size transparent layer per suit,
    positioned at grid intersections using alignment. """
    controls = []
    for r, c in PIP_POSITIONS[rank]:
        x = c - 2                 # 列 1/2/3 → -1 / 0 / +1
        y = (r - 1) / 3 - 1       # 行 1~7   → -1 ~ +1
        controls.append(
            ft.Container(
                width=box_w, height=box_h,
                alignment=ft.Alignment(x, y),
                content=ft.Text(
                    suit, size=16, color=color,
                    rotate=ft.Rotate(angle=math.pi) if r >= 5 else None,
                ),
            )
        )
    return ft.Stack(controls=controls, clip_behavior=ft.ClipBehavior.NONE)


def create_card() -> tuple[ft.Container, int]:
    """ Generate a 1-10 rank card.
    返回 (牌面容器, 牌面数字)。牌面数字用于核对玩家输入并调用 solve_24。
    """
    rank = random.randint(1, 10)
    suit = random.choice(SUITS)
    color = suit_color(suit)
    label = rank_label(rank)
    card = ft.Container(
        width=CARD_W,
        height=CARD_H,
        bgcolor=CARD_WHITE,
        border=ft.Border.all(CARD_BORDER_THICK, CARD_BORDER),
        border_radius=ft.BorderRadius.all(14),
        content=ft.Stack(
            controls=[
                ft.Container(left=6, top=6, content=make_corner(label, suit, color)),
                ft.Container(
                    right=6,
                    bottom=6,
                    rotate=ft.Rotate(angle=math.pi),
                    content=make_corner(label, suit, color),
                ),
                ft.Container(
                    left=((CARD_W - 2 * CARD_BORDER_THICK) - CARD_W * 0.54) / 2,
                    top=((CARD_H - 2 * CARD_BORDER_THICK) - CARD_H * 0.78) / 2,
                    width=CARD_W * 0.54,
                    height=CARD_H * 0.78,
                    content=make_pip_grid(suit, color, rank, CARD_W * 0.54, CARD_H * 0.78),
                ),
            ],
        ),
    )
    return card, rank


def solve_24(ranks) -> list:
    """ 采用穷举法，返回算式字符串列表，无解返回空列表。 """
    solutions = []
    for nums in itertools.permutations(ranks):          # 四个数的全排列
        for ops in itertools.product('+-*/', repeat=3):  # 三个运算符（可重复）
            bds1 = '({0}{4}{1}){5}({2}{6}{3})'.format(*nums, *ops)   # (a?b)?(c?d)
            bds2 = '(({0}{4}{1}){5}{2}){6}{3}'.format(*nums, *ops)   # ((a?b)?c)?d
            bds3 = '{0}{4}({1}{5}({2}{6}{3}))'.format(*nums, *ops)   # a?(b?(c?d))
            bds4 = '({0}{4}({1}{5}{2})){6}{3}'.format(*nums, *ops)   # (a?(b?c))?d
            bds5 = '{0}{4}(({1}{5}{2}){6}{3})'.format(*nums, *ops)   # a?((b?c)?d)
            for bds in [bds1, bds2, bds3, bds4, bds5]:
                try:
                    if abs(eval(bds) - 24.0) < 1e-10:   # 消除浮点误差
                        solutions.append(bds)
                except ZeroDivisionError:
                    continue
    return sorted(set(solutions))


def verify_solution(expr: str, ranks: list) -> tuple[bool, str]:
    """ 校验玩家输入：数字必须与牌面一致，且算式结果等于 24。
    返回 (是否通过, 提示信息)。
    """
    expr = (expr or "").strip()
    if not expr:
        return False, "请输入算式"

    # 字符白名单：数字、四则运算、括号、空格（不含小数点，牌面均为整数）
    allowed = set("0123456789+-*/() ")
    for ch in expr:
        if ch not in allowed:
            return False, f"包含非法字符「{ch}」"

    # 提取所有数字，个数必须为 4
    numbers = re.findall(r'\d+', expr)
    if len(numbers) != 4:
        return False, "必须恰好使用 4 个数字"

    # 数字多重集必须与牌面一致
    used = sorted(int(n) for n in numbers)
    expected = sorted(ranks)
    if used != expected:
        return False, f"数字 {used} 与牌面 {expected} 不一致"

    try:
        value = eval(expr)
    except ZeroDivisionError:
        return False, "算式中出现除零"
    except Exception:
        return False, "算式无法计算"

    if abs(value - 24.0) < 1e-9:
        return True, f"{expr} = 24，正确！"
    return False, f"{expr} = {value}，不等于 24"


def main(page: ft.Page):
    page.title = "24-point Card Game"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # 当前四张牌的牌面数字（由 create_card 返回）
    current_ranks: list = []

    title_text = ft.Text(
        "24 points Card Game\n       24点纸牌游戏",
        size=36,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700,
        visible=False,
    )

    cards_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        visible=False,
    )

    # 玩家解法输入框
    solution_input = ft.TextField(
        hint_text="请输入算式，如 (9-8)*8*3（A 记作 1）",
        width=420,
        text_style=ft.TextStyle(size=16),
        visible=False,
    )

    # 核对 / 提示 按钮
    check_button = ft.Button(
        content="Check 核对",
        icon=ft.Icons.CHECK,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            padding=ft.Padding.symmetric(horizontal=20, vertical=10),
        ),
    )
    hint_button = ft.Button(
        content="Hint 查看所有解法",
        icon=ft.Icons.LIGHTBULB,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.ORANGE_600,
            color=ft.Colors.WHITE,
            padding=ft.Padding.symmetric(horizontal=20, vertical=10),
        ),
    )
    buttons_row = ft.Row(
        controls=[check_button, hint_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        visible=False,
    )

    # 核对结果反馈
    feedback_text = ft.Text("", size=16, visible=False)

    # 所有解法展示
    hint_text = ft.Text("", size=14, visible=False)

    def on_click(e):
        # 重新发牌，并记录牌面数字
        cards_row.controls = []
        current_ranks.clear()
        for _ in range(4):
            card, rank = create_card()
            cards_row.controls.append(card)
            current_ranks.append(rank)

        title_text.visible = True
        cards_row.visible = True
        solution_input.visible = True
        buttons_row.visible = True
        feedback_text.visible = True
        hint_text.visible = True

        # 清空上次的输入与结果
        solution_input.value = ""
        feedback_text.value = ""
        hint_text.value = ""
        click_button.content = "Redeal 重新发牌 🎴"
        page.update()

    def on_check(e):
        ok, msg = verify_solution(solution_input.value, current_ranks)
        feedback_text.value = ("✓ " if ok else "✗ ") + msg
        feedback_text.color = ft.Colors.GREEN_700 if ok else ft.Colors.RED_700
        page.update()

    def on_hint(e):
        if not current_ranks:
            return
        sols = solve_24(current_ranks)
        if not sols:
            hint_text.value = "No Solution! 无解!"
            hint_text.color = ft.Colors.RED_700
        else:
            hint_text.value = (
                f"牌面 {current_ranks}，共 {len(sols)} 种解法：\n"
                + "\n".join(sols)
            )
            hint_text.color = ft.Colors.BLUE_700
        page.update()

    click_button = ft.Button(
        content="Click here to start 24 points card game",
        icon=ft.Icons.CASINO,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            padding=ft.Padding.symmetric(horizontal=24, vertical=12),
            text_style=ft.TextStyle(size=18),
        ),
    )
    check_button.on_click = on_check
    hint_button.on_click = on_hint

    page.add(
        ft.Column(
            controls=[
                click_button,
                ft.Container(height=20),
                title_text,
                ft.Container(height=20),
                cards_row,
                ft.Container(height=20),
                solution_input,
                ft.Container(height=10),
                buttons_row,
                ft.Container(height=16),
                feedback_text,
                ft.Container(height=8),
                hint_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)
