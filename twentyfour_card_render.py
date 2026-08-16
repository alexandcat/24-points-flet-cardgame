"""
twentyfour_card_render.py
24 Points card face renderer with Flet
Render standard playing card pip layout(A‑10), corner markers, suit symbols.
Reference: 52CardEngine card layout
Run: python twentyfour_card_render.py
"""

import math
import random
import flet as ft


# Color scheme
CARD_WHITE = "#F2F2F2"    # Card background 牌面背景 (242, 242, 242)
CARD_BORDER = "#D3D3D3"   # Border 边框 (211, 211, 211)
CARD_RED = "#C72C48"      # Hearts/Diamonds 红心/方块 (199, 44, 72)
CARD_BLACK = "#1C1C1E"    # Spades/Clubs 黑桃/梅花 (28, 28, 30)

SUITS = ["♠", "♥", "♦", "♣"]

CARD_W, CARD_H = 90, 126  # Card dimensions 牌面尺寸
CARD_BORDER_THICK = 2     # Card border thickness 纸牌边框厚度

# 3 列 × 7 行阵列：每个点数对应的花色位置（行 1-7，列 1-3）
# 数字 1 放正中央 (4,2)；数字 2 放第 1 行第 2 列和第 7 行第 2 列；
# 其余按对称递推排列，花色数量与点数一致。
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
    """点数映射：1 记为 A。 """
    return "A" if rank == 1 else str(rank)


def suit_color(suit: str) -> str:
    """红心/方块为红色，黑桃/梅花为黑色。"""
    return CARD_RED if suit in ("♥", "♦") else CARD_BLACK


def make_corner(label: str, suit: str, color: str) -> ft.Column:
    """角落标记：点数 + 花色，竖排。"""
    return ft.Column(
        controls=[
            # ft.Text增加style...height=0.9, 增加条件判断：label=10时，减小字符宽度的参数,定位锚定左缘
            ft.Text(label, size=15, weight=ft.FontWeight.BOLD, color=color, 
                    style=ft.TextStyle(height=0.9), 
                    scale=ft.Scale(scale_x=0.75, alignment=ft.Alignment.CENTER_LEFT) if label == "10" else None,),
            ft.Text(suit, size=10, color=color, style=ft.TextStyle(height=0.9)),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# 中央花色改为stack生成模式
def make_pip_grid(suit: str, color: str, rank: int,
                  box_w: float, box_h: float) -> ft.Stack:
    """浮层模式：每个花色一个全尺寸透明层，用 alignment 定位到网格交点。
    列表顺序 = 绘制顺序（前=底层，后=顶层）；透明区域不影响其他层。"""
    controls = []
    for r, c in PIP_POSITIONS[rank]:
        x = c - 2                 # 列 1/2/3 → -1 / 0 / +1
        y = (r - 1) / 3 - 1       # 行 1~7   → -1 ~ +1（6 个等分点）
        controls.append(
            ft.Container(
                width=box_w, height=box_h,        # 全尺寸透明层
                alignment=ft.Alignment(x, y),     # 花色中心落到网格交点
                content=ft.Text(
                    suit, size=16, color=color,
                    rotate=ft.Rotate(angle=math.pi) if r >= 5 else None,
                ),
            )
        )
    return ft.Stack(controls=controls, clip_behavior=ft.ClipBehavior.NONE)


def create_card() -> ft.Container:
    """生成一张 1~10 点的纸牌，牌面 UI 参照 52CardEngine。"""
    rank = random.randint(1, 10)
    suit = random.choice(SUITS)
    color = suit_color(suit)
    label = rank_label(rank)

    return ft.Container(
        width=CARD_W,
        height=CARD_H,
        bgcolor=CARD_WHITE,
        border=ft.Border.all(CARD_BORDER_THICK, CARD_BORDER),
        border_radius=ft.BorderRadius.all(14),
        content=ft.Stack(
            controls=[
                # 左上角：点数 + 花色
                ## 增加 label=10, 定位向左偏的条件判断
                ft.Container(left=6, top=6, content=make_corner(label, suit, color)),
                # 右下角：旋转 180° 的镜像标记
                ft.Container(
                    right=6,
                    bottom=6,
                    rotate=ft.Rotate(angle=math.pi),
                    content=make_corner(label, suit, color),
                ),
                # 中央：子容器（宽度为父容器 54%、高度为 78%），
                # 内部 7 行 3 列网格，按点数在对应位置显示花色
                ft.Container(
                    left=((CARD_W - 2 * CARD_BORDER_THICK) - CARD_W * 0.54) / 2,  # 容器定位需减去边框厚度
                    top=((CARD_H - 2 * CARD_BORDER_THICK) - CARD_H * 0.78) / 2,  # 容器定位需减去边框厚度
                    width=CARD_W * 0.54,
                    height=CARD_H * 0.78,
                    content=make_pip_grid(suit, color, rank, CARD_W * 0.54, CARD_H * 0.78),  # 传入实际尺寸
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.title = "24-point Card Game"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Title text (initially hidden) 标题文字（初始隐藏）
    title_text = ft.Text(
        "24 points Card Game\n       24点纸牌游戏",
        size=36,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700,
        visible=False,
    )

    # Card display row (initially hidden; shows 4 cards side by side after click)
    # （初始隐藏，点击后并列显示 4 张牌）
    cards_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        visible=False,
    )

    # Button click handler
    def on_click(e):
        cards_row.controls = [create_card() for _ in range(4)]
        title_text.visible = True
        cards_row.visible = True
        click_button.content = "Redeal 重新发牌 🎴"
        page.update()

    # Button
    click_button = ft.Button(
        content="Start dealing 开始发牌",
        icon=ft.Icons.CASINO,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            padding=ft.Padding.symmetric(horizontal=24, vertical=12),
            text_style=ft.TextStyle(size=18),
        ),
    )

    # Page layout
    page.add(
        ft.Column(
            controls=[
                click_button,
                ft.Container(height=20),
                title_text,
                ft.Container(height=20),
                cards_row,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)
