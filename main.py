from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote

import flet as ft


BASE_W = 1693
BASE_H = 929
DESKTOP_BREAKPOINT = 980

ORANGE = "#ff7a00"
NAVY = "#143a6d"
TEXT = "#20385f"
LIGHT = "#dcdcdc"
WHITE = "#ffffff"
SOFT_PANEL = "#fbfbfb"
NAV_ITEMS = (
    ("ABOUT ME", "about"),
    ("CV", "cv"),
    ("AWARDS", "awards"),
)

CERTIFICATE_COLUMNS = (
    (
        ("Best in Civil year one", "certificates/Best in Civil year one.pdf"),
        ("Third best in Material Science", "certificates/third best in Material Scirnce.pdf"),
        ("Teamwork", "certificates/teamwork.pdf"),
    ),
    (
        ("Ordinary level certificate", "certificates/ordinary level certificate.pdf"),
        ("AS level certificate", "certificates/AS level certificate.pdf"),
        ("AS level certificate 2", "certificates/AS level certificate 2.pdf"),
    ),
)


@dataclass
class UiState:
    nav_open: bool = False
    active_section: str = "about"


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def page_width(page: ft.Page) -> float:
    return float(page.width or getattr(page.window, "width", None) or BASE_W)


def page_height(page: ft.Page) -> float:
    return float(page.height or getattr(page.window, "height", None) or BASE_H)


def desktop_scale(width: float) -> float:
    return clamp(width / BASE_W, 0.82, 1.0)


def mobile_scale(width: float) -> float:
    return clamp(width / 430.0, 0.84, 1.0)


def scale_value(value: float, scale: float) -> float:
    return value * scale


def asset_url(relative_path: str) -> str:
    return "/".join(quote(part) for part in relative_path.split("/"))


def desktop_nav_item(label: str, *, active: bool, scale: float, on_tap) -> ft.GestureDetector:
    return ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.CLICK,
        on_tap=on_tap,
        content=ft.Column(
        spacing=8 * scale,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                label,
                size=23 * scale,
                weight=ft.FontWeight.BOLD,
                font_family="MontserratBold",
                color=ORANGE if active else NAVY,
                no_wrap=True,
            ),
            ft.Container(
                width=148 * scale,
                height=4 * scale,
                bgcolor=ORANGE,
                opacity=1.0 if active else 0.0,
                border_radius=ft.BorderRadius.all(999),
            ),
        ],
        ),
    )


def desktop_header(scale: float, active_section: str, navigate_to) -> ft.Container:
    return ft.Container(
        width=None,
        padding=ft.padding.only(
            left=scale_value(40, scale),
            right=scale_value(48, scale),
            top=scale_value(28, scale),
            bottom=scale_value(14, scale),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=scale_value(70, scale),
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        desktop_nav_item(
                            "ABOUT ME",
                            active=active_section == "about",
                            scale=scale,
                            on_tap=lambda e: navigate_to("about"),
                        ),
                        desktop_nav_item(
                            "CV",
                            active=active_section == "cv",
                            scale=scale,
                            on_tap=lambda e: navigate_to("cv"),
                        ),
                        desktop_nav_item(
                            "AWARDS",
                            active=active_section == "awards",
                            scale=scale,
                            on_tap=lambda e: navigate_to("awards"),
                        ),
                    ],
                ),
            ],
        ),
    )


def mobile_header(scale: float, nav_open: bool, toggle_nav) -> ft.Container:
    return ft.Container(
        padding=ft.padding.only(
            left=scale_value(18, scale),
            right=scale_value(14, scale),
            top=scale_value(18, scale),
            bottom=scale_value(12, scale),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.CLOSE if nav_open else ft.Icons.MENU,
                    icon_color=NAVY,
                    icon_size=30 * scale,
                    on_click=toggle_nav,
                    tooltip="Close navigation" if nav_open else "Open navigation",
                ),
            ],
        ),
    )


def mobile_nav_panel(
    scale: float,
    active_section: str,
    navigate_to,
    *,
    panel_width: float | None = None,
    top: float | None = None,
) -> ft.Container:
    item_width = None if panel_width is None else max(0, panel_width - scale_value(28, scale))

    def menu_item(label: str, key: str) -> ft.Container:
        active = active_section == key
        return ft.Container(
            width=item_width,
            padding=ft.padding.symmetric(
                horizontal=scale_value(14, scale),
                vertical=scale_value(12, scale),
            ),
            border_radius=18,
            bgcolor="#fff6ee" if active else WHITE,
            on_click=lambda e: navigate_to(key, close_nav=True),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        label,
                        size=18 * scale,
                        weight=ft.FontWeight.BOLD,
                        font_family="MontserratBold",
                        color=ORANGE if active else NAVY,
                        no_wrap=True,
                    ),
                    ft.Container(
                        width=12 * scale,
                        height=12 * scale,
                        bgcolor=ORANGE if active else LIGHT,
                        border_radius=ft.BorderRadius.all(999),
                    ),
                ],
            ),
        )

    return ft.Container(
        left=scale_value(18, scale),
        top=top if top is not None else scale_value(108, scale),
        width=panel_width,
        padding=ft.padding.all(scale_value(14, scale)),
        border_radius=22,
        bgcolor=SOFT_PANEL,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=18 * scale,
            color="#18000000",
            offset=ft.Offset(0, 6 * scale),
        ),
        content=ft.Column(
            spacing=scale_value(10, scale),
            controls=[
                menu_item("ABOUT ME", "about"),
                menu_item("CV", "cv"),
                menu_item("AWARDS", "awards"),
            ],
        ),
    )


def hero_copy(
    scale: float,
    *,
    centered: bool,
    mobile: bool,
    available_width: float | None = None,
) -> ft.Column:
    greeting_size = (30 if mobile else 38) * scale
    name_size = (38 if mobile else 78) * scale
    subtitle_size = (19 if mobile else 27) * scale
    body_size = (16 if mobile else 22) * scale

    align = ft.CrossAxisAlignment.CENTER if centered else ft.CrossAxisAlignment.START
    text_align = ft.TextAlign.CENTER if centered else ft.TextAlign.START
    body_width = (
        clamp(available_width or scale_value(620, scale), scale_value(220, scale), scale_value(620, scale))
        if mobile
        else scale_value(620, scale)
    )

    name_row = ft.Row(
        width=available_width if centered else None,
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER if centered else ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "ANGULA.T.",
                size=name_size,
                weight=ft.FontWeight.BOLD,
                font_family="MontserratBold",
                color=ORANGE,
                no_wrap=True,
            ),
            ft.Text(
                "FRIEDA",
                size=name_size,
                weight=ft.FontWeight.BOLD,
                font_family="MontserratBold",
                color=NAVY,
                no_wrap=True,
            ),
        ],
    )

    return ft.Column(
        spacing=0,
        horizontal_alignment=align,
        controls=[
            ft.Text(
                "Hello, I'm",
                size=greeting_size,
                weight=ft.FontWeight.BOLD,
                font_family="MontserratBold",
                color=NAVY,
                no_wrap=True,
                text_align=text_align,
            ),
            ft.Container(height=scale_value(28 if mobile else 24, scale)),
            name_row,
            ft.Container(height=scale_value(22 if mobile else 20, scale)),
            ft.Container(
                width=scale_value(72 if mobile else 72, scale),
                height=scale_value(5, scale),
                bgcolor=ORANGE,
                border_radius=ft.BorderRadius.all(999),
            ),
            ft.Container(height=scale_value(26 if mobile else 28, scale)),
            ft.Text(
                "Second-Year Metallurgical Engineering Student",
                size=subtitle_size,
                weight=ft.FontWeight.BOLD,
                font_family="MontserratBold",
                color=NAVY,
                text_align=text_align,
                max_lines=2,
            ),
            ft.Container(height=scale_value(26 if mobile else 30, scale)),
            ft.Text(
                "A Second-Year Metallurgical Engineering student at UNAM with a proven record of academic excellence. Recognized as the top performer in Civil Engineering year one and ranked among the top three in Material Science. Dedicated to delivering innovative, precision-driven solutions in engineering.",
                size=body_size,
                font_family="Montserrat",
                color=TEXT,
                width=body_width,
                text_align=text_align,
            ),
            ft.Container(height=scale_value(12 if mobile else 16, scale)),
        ],
    )


def portrait_shell(scale: float, size: float) -> ft.Container:
    photo_size = size * 0.90
    return ft.Container(
        width=size,
        height=size,
        shape=ft.BoxShape.CIRCLE,
        bgcolor=WHITE,
        alignment=ft.Alignment.CENTER,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=24 * scale,
            color="#22000000",
            offset=ft.Offset(0, 8 * scale),
        ),
        content=ft.Container(
            width=photo_size,
            height=photo_size,
            shape=ft.BoxShape.CIRCLE,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Image(
                src="portrait.jpeg",
                width=photo_size,
                height=photo_size,
                fit=ft.BoxFit.COVER,
                filter_quality=ft.FilterQuality.HIGH,
            ),
        ),
    )


def desktop_hero(scale: float, width: float) -> ft.Container:
    portrait_size = clamp(width * 0.33, scale_value(270, scale), scale_value(554, scale))

    return ft.Container(
        expand=True,
        padding=ft.padding.only(
            top=scale_value(136, scale),
            left=0,
            right=0,
            bottom=scale_value(18, scale),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    expand=True,
                    padding=ft.padding.only(left=scale_value(83, scale)),
                    content=hero_copy(
                        scale,
                        centered=False,
                        mobile=False,
                    ),
                ),
                ft.Container(
                    padding=ft.padding.only(
                        top=scale_value(6, scale),
                        right=scale_value(42, scale),
                    ),
                    content=portrait_shell(scale, portrait_size),
                ),
            ],
        ),
    )


def mobile_hero(scale: float, width: float) -> ft.Container:
    portrait_size = clamp(
        width - scale_value(56, scale),
        scale_value(250, scale),
        scale_value(360, scale),
    )
    available_width = width - scale_value(56, scale)

    return ft.Container(
        expand=True,
        padding=ft.padding.only(
            left=scale_value(24, scale),
            right=scale_value(24, scale),
            top=scale_value(18, scale),
            bottom=scale_value(24, scale),
        ),
        content=ft.Column(
            spacing=scale_value(22, scale),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                hero_copy(
                    scale,
                    centered=True,
                    mobile=True,
                    available_width=available_width,
                ),
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    padding=ft.padding.only(top=scale_value(8, scale)),
                    content=portrait_shell(scale, portrait_size),
                ),
            ],
        ),
    )


def section_card(
    scale: float,
    title: str,
    body: str,
    accent: str,
    *,
    width: float | None = None,
) -> ft.Container:
    return ft.Container(
        expand=width is None,
        width=width,
        padding=ft.padding.all(scale_value(24, scale)),
        border_radius=24,
        bgcolor=WHITE,
        border=ft.border.all(1, "#e5e5e5"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=14 * scale,
            color="#16000000",
            offset=ft.Offset(0, 4 * scale),
        ),
        content=ft.Column(
            spacing=scale_value(12, scale),
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=scale_value(58, scale),
                    height=scale_value(5, scale),
                    bgcolor=accent,
                    border_radius=ft.BorderRadius.all(999),
                ),
                ft.Text(
                    title,
                    size=22 * scale,
                    weight=ft.FontWeight.BOLD,
                    font_family="MontserratBold",
                    color=NAVY,
                ),
                ft.Text(
                    body,
                    size=16 * scale,
                    font_family="Montserrat",
                    color=TEXT,
                    max_lines=4,
                ),
            ],
        ),
    )


def section_block(
    scale: float,
    *,
    key: str,
    label: str,
    title: str,
    subtitle: str,
    cards: list[tuple[str, str, str]],
    width: float,
    mobile: bool,
    alternate: bool = False,
) -> ft.Container:
    horizontal_padding = scale_value(24 if mobile else 80, scale)
    vertical_padding = scale_value(46 if mobile else 68, scale)

    card_controls = [
        section_card(
            scale,
            card_title,
            card_body,
            accent,
            width=None if not mobile else width - (horizontal_padding * 2),
        )
        for card_title, card_body, accent in cards
    ]

    cards_layout: ft.Control
    if mobile:
        cards_layout = ft.Column(
            spacing=scale_value(14, scale),
            controls=card_controls,
        )
    else:
        cards_layout = ft.Row(
            spacing=scale_value(18, scale),
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=card_controls,
        )

    return ft.Container(
        key=key,
        width=width,
        bgcolor=SOFT_PANEL if alternate else WHITE,
        padding=ft.padding.symmetric(
            horizontal=horizontal_padding,
            vertical=vertical_padding,
        ),
        content=ft.Column(
            spacing=scale_value(24, scale),
            controls=[
                ft.Column(
                    spacing=scale_value(10, scale),
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            label,
                            size=18 * scale,
                            weight=ft.FontWeight.BOLD,
                            font_family="MontserratBold",
                            color=ORANGE,
                        ),
                        ft.Text(
                            title,
                            size=(28 if mobile else 40) * scale,
                            weight=ft.FontWeight.BOLD,
                            font_family="MontserratBold",
                            color=NAVY,
                        ),
                        ft.Container(
                            width=scale_value(84, scale),
                            height=scale_value(5, scale),
                            bgcolor=ORANGE,
                            border_radius=ft.BorderRadius.all(999),
                        ),
                        ft.Text(
                            subtitle,
                            size=(16 if mobile else 20) * scale,
                            font_family="Montserrat",
                            color=TEXT,
                        ),
                    ],
                ),
                cards_layout,
            ],
        ),
    )


def cv_section(scale: float, *, mobile: bool, width: float, open_cv_pdf) -> ft.Container:
    horizontal_padding = scale_value(18 if mobile else 56, scale)
    vertical_padding = scale_value(24 if mobile else 42, scale)
    card_width = clamp(width - (horizontal_padding * 2), scale_value(280, scale), scale_value(760, scale))

    return ft.Container(
        expand=True,
        padding=ft.padding.symmetric(
            horizontal=horizontal_padding,
            vertical=vertical_padding,
        ),
        alignment=ft.Alignment.CENTER,
        content=ft.Container(
            width=card_width,
            padding=ft.padding.all(scale_value(24, scale)),
            border_radius=24,
            bgcolor=WHITE,
            border=ft.border.all(1, "#e5e5e5"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=16 * scale,
                color="#17000000",
                offset=ft.Offset(0, 5 * scale),
            ),
            content=ft.Column(
                spacing=scale_value(18, scale),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER if mobile else ft.CrossAxisAlignment.START,
                controls=[
                    ft.Column(
                        spacing=scale_value(10, scale),
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER if mobile else ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Text(
                                "CV",
                                size=(24 if mobile else 36) * scale,
                                weight=ft.FontWeight.BOLD,
                                font_family="MontserratBold",
                                color=NAVY,
                            ),
                            ft.Container(
                                width=scale_value(72, scale),
                                height=scale_value(5, scale),
                                bgcolor=ORANGE,
                                border_radius=ft.BorderRadius.all(999),
                            ),
                        ],
                    ),
                    cv_open_panel(scale, open_cv_pdf, mobile),
                ],
            ),
        ),
    )


def awards_section(
    scale: float,
    *,
    mobile: bool,
    width: float,
    open_certificates_pdf,
    open_pdf,
) -> ft.Container:
    horizontal_padding = scale_value(18 if mobile else 56, scale)
    vertical_padding = scale_value(24 if mobile else 42, scale)
    card_width = clamp(width - (horizontal_padding * 2), scale_value(280, scale), scale_value(760, scale))

    return ft.Container(
        expand=True,
        padding=ft.padding.symmetric(
            horizontal=horizontal_padding,
            vertical=vertical_padding,
        ),
        alignment=ft.Alignment.CENTER,
        content=ft.Container(
            width=card_width,
            padding=ft.padding.all(scale_value(24, scale)),
            border_radius=24,
            bgcolor=WHITE,
            border=ft.border.all(1, "#e5e5e5"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=16 * scale,
                color="#17000000",
                offset=ft.Offset(0, 5 * scale),
            ),
            content=ft.Column(
                spacing=scale_value(16, scale),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER if mobile else ft.CrossAxisAlignment.START,
                controls=[
                    ft.Column(
                        spacing=scale_value(10, scale),
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER if mobile else ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Text(
                                "AWARDS",
                                size=(24 if mobile else 36) * scale,
                                weight=ft.FontWeight.BOLD,
                                font_family="MontserratBold",
                                color=NAVY,
                            ),
                            ft.Container(
                                width=scale_value(72, scale),
                                height=scale_value(5, scale),
                                bgcolor=ORANGE,
                                border_radius=ft.BorderRadius.all(999),
                            ),
                            ft.Text(
                                "Tap a certificate to open its full PDF.",
                                size=(14 if mobile else 17) * scale,
                                font_family="Montserrat",
                                color=TEXT,
                                text_align=ft.TextAlign.CENTER if mobile else ft.TextAlign.START,
                            ),
                        ],
                    ),
                    document_open_panel(scale, "VIEW CERTIFICATES", open_certificates_pdf, mobile),
                    certificate_gallery(scale, mobile=mobile, open_pdf=open_pdf),
                ],
            ),
        ),
    )


def document_open_panel(scale: float, button_label: str, open_pdf, mobile: bool) -> ft.Container:
    button_width = scale_value(240 if mobile else 280, scale)
    return ft.Container(
        width=button_width,
        padding=ft.padding.symmetric(
            horizontal=scale_value(18, scale),
            vertical=scale_value(14, scale),
        ),
        border_radius=18,
        bgcolor=ORANGE,
        on_click=open_pdf,
        content=ft.Row(
            spacing=scale_value(10, scale),
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.PICTURE_AS_PDF,
                    color=WHITE,
                    size=22 * scale,
                ),
                ft.Text(
                    button_label,
                    size=(16 if mobile else 18) * scale,
                    weight=ft.FontWeight.BOLD,
                    font_family="MontserratBold",
                    color=WHITE,
                    no_wrap=True,
                ),
            ],
        ),
    )


def cv_open_panel(scale: float, open_cv_pdf, mobile: bool) -> ft.Container:
    return document_open_panel(scale, "VIEW CV", open_cv_pdf, mobile)


def certificate_tile(
    scale: float,
    label: str,
    relative_path: str,
    open_pdf,
    *,
    mobile: bool,
) -> ft.GestureDetector:
    icon_size = (22 if mobile else 24) * scale
    title_size = (14 if mobile else 16) * scale
    subtitle_size = (11 if mobile else 13) * scale

    return ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.CLICK,
        on_tap=lambda e: open_pdf(relative_path),
        content=ft.Container(
            expand=True,
            padding=ft.padding.symmetric(
                horizontal=scale_value(14, scale),
                vertical=scale_value(12, scale),
            ),
            border_radius=18,
            bgcolor=WHITE,
            border=ft.border.all(1, "#e7e7e7"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10 * scale,
                color="#12000000",
                offset=ft.Offset(0, 3 * scale),
            ),
            content=ft.Row(
                spacing=scale_value(12, scale),
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=scale_value(44 if mobile else 48, scale),
                        height=scale_value(44 if mobile else 48, scale),
                        alignment=ft.Alignment.CENTER,
                        bgcolor="#fff2e6",
                        border_radius=16,
                        content=ft.Icon(
                            ft.Icons.PICTURE_AS_PDF,
                            color=ORANGE,
                            size=icon_size,
                        ),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=scale_value(2, scale),
                        controls=[
                            ft.Text(
                                label,
                                size=title_size,
                                weight=ft.FontWeight.BOLD,
                                font_family="MontserratBold",
                                color=NAVY,
                                max_lines=2,
                            ),
                            ft.Text(
                                "Open PDF",
                                size=subtitle_size,
                                font_family="Montserrat",
                                color=TEXT,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )


def certificate_gallery(
    scale: float,
    *,
    mobile: bool,
    open_pdf,
) -> ft.Container:
    column_gap = scale_value(16 if mobile else 20, scale)
    row_gap = scale_value(12 if mobile else 14, scale)

    left_column = ft.Column(
        spacing=row_gap,
        expand=True,
        controls=[
            certificate_tile(scale, label, relative_path, open_pdf, mobile=mobile)
            for label, relative_path in CERTIFICATE_COLUMNS[0]
        ],
    )
    right_column = ft.Column(
        spacing=row_gap,
        expand=True,
        controls=[
            certificate_tile(scale, label, relative_path, open_pdf, mobile=mobile)
            for label, relative_path in CERTIFICATE_COLUMNS[1]
        ],
    )

    return ft.Container(
        expand=True,
        content=ft.Row(
            spacing=column_gap,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(expand=True, content=left_column),
                ft.Container(expand=True, content=right_column),
            ],
        ),
    )


def build_layout(
    page: ft.Page,
    state: UiState,
    navigate_to,
    toggle_nav,
    open_cv_pdf,
    open_certificates_pdf,
    open_pdf,
) -> ft.Control:
    width = page_width(page)
    height = page_height(page)
    desktop = width >= DESKTOP_BREAKPOINT
    scale = desktop_scale(width) if desktop else mobile_scale(width)

    if desktop:
        state.nav_open = False

    background_asset = "background.svg" if desktop else "background-mobile.svg"
    background = ft.Image(
        src=background_asset,
        left=0,
        top=0,
        width=width,
        height=height,
        fit=ft.BoxFit.FILL,
        filter_quality=ft.FilterQuality.HIGH,
    )

    if state.active_section == "cv":
        main_view = cv_section(
            scale,
            mobile=not desktop,
            width=width,
            open_cv_pdf=open_cv_pdf,
        )
    elif state.active_section == "awards":
        main_view = awards_section(
            scale,
            mobile=not desktop,
            width=width,
            open_certificates_pdf=open_certificates_pdf,
            open_pdf=open_pdf,
        )
    else:
        main_view = desktop_hero(scale, width) if desktop else mobile_hero(scale, width)

    header = (
        desktop_header(scale, state.active_section, navigate_to)
        if desktop
        else mobile_header(scale, state.nav_open, toggle_nav)
    )

    stage_controls = [
        background,
        ft.Container(
            expand=True,
            content=ft.Column(
                spacing=0,
                expand=True,
                controls=[
                    header,
                    ft.Container(expand=True, content=main_view),
                ],
            ),
        ),
    ]

    if not desktop and state.nav_open:
        stage_controls.append(
            mobile_nav_panel(
                scale,
                state.active_section,
                navigate_to,
                panel_width=width - scale_value(36, scale),
                top=scale_value(104, scale),
            )
        )

    return ft.Container(
        expand=True,
        content=ft.Stack(
            width=width,
            height=height,
            clip_behavior=ft.ClipBehavior.NONE,
            controls=stage_controls,
        ),
    )


def main(page: ft.Page) -> None:
    state = UiState()

    page.title = "Angula T. Frieda"
    page.bgcolor = WHITE
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.HIDDEN
    page.theme = ft.Theme(font_family="Montserrat")
    page.fonts = {
        "Montserrat": "/fonts/Montserrat-Regular.ttf",
        "MontserratBold": "/fonts/Montserrat-Bold.ttf",
    }

    def open_pdf(relative_path: str) -> None:
        page.run_task(
            page.url_launcher.launch_url,
            ft.Url(url=asset_url(relative_path), target=ft.UrlTarget.BLANK),
        )

    def open_cv_pdf(_: ft.ControlEvent | None = None) -> None:
        open_pdf("cv/cv-opp.pdf")

    def open_certificates_pdf(_: ft.ControlEvent | None = None) -> None:
        open_pdf("certificates/certificates.pdf")

    def rebuild(_: ft.ControlEvent | None = None) -> None:
        page.controls.clear()
        page.add(
            build_layout(
                page,
                state,
                navigate_to,
                toggle_nav,
                open_cv_pdf,
                open_certificates_pdf,
                open_pdf,
            )
        )
        page.update()

    def toggle_nav(_: ft.ControlEvent | None = None) -> None:
        state.nav_open = not state.nav_open
        rebuild()

    def navigate_to(section_key: str, close_nav: bool = False) -> None:
        state.active_section = section_key
        if close_nav:
            state.nav_open = False
        rebuild()

    page.on_resize = rebuild
    rebuild()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
