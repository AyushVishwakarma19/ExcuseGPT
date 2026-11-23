"""ExcuseGPT Brand Identity and Vector Asset System.

Provides a fresh, sunlit geometric SVG brand identity, wordmark, and unified
stroke-based icon library designed for ExcuseGPT's light editorial SaaS theme.
"""

# Sunlit Geometric Mark (36x36 viewBox)
_LOGO_MARK_RAW = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="{size}" height="{size}" fill="none" style="vertical-align: middle; flex-shrink: 0;">
  <rect x="1" y="1" width="34" height="34" rx="10" fill="#FEF9C3" stroke="#EAB308" stroke-width="1.5"/>
  <path d="M9 11.5C9 9.567 10.567 8 12.5 8H23.5C25.433 8 27 9.567 27 11.5V20.5C27 22.433 25.433 24 23.5 24H16.5L11.5 28V24H12.5C10.567 24 9 22.433 9 20.5V11.5Z" fill="#18181B"/>
  <rect x="13" y="12.5" width="10" height="2.2" rx="1.1" fill="#FACC15"/>
  <rect x="13" y="16.8" width="6.5" height="2.2" rx="1.1" fill="#FAF9F5"/>
  <circle cx="22.2" cy="17.9" r="1.3" fill="#FACC15"/>
</svg>
"""

# Horizontal Brand Mark + Clean Editorial Wordmark SVG (210x40)
_LOGO_FULL_RAW = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 40" width="{width}" height="{height}" fill="none" style="vertical-align: middle; flex-shrink: 0;">
  <g transform="translate(2, 2)">
    <rect x="1" y="1" width="34" height="34" rx="10" fill="#FEF9C3" stroke="#EAB308" stroke-width="1.5"/>
    <path d="M9 11.5C9 9.567 10.567 8 12.5 8H23.5C25.433 8 27 9.567 27 11.5V20.5C27 22.433 25.433 24 23.5 24H16.5L11.5 28V24H12.5C10.567 24 9 22.433 9 20.5V11.5Z" fill="#18181B"/>
    <rect x="13" y="12.5" width="10" height="2.2" rx="1.1" fill="#FACC15"/>
    <rect x="13" y="16.8" width="6.5" height="2.2" rx="1.1" fill="#FAF9F5"/>
    <circle cx="22.2" cy="17.9" r="1.3" fill="#FACC15"/>
  </g>
  <text x="46" y="25.5" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif" font-size="19" font-weight="800" fill="{text_color}" letter-spacing="-0.03em">Excuse</text>
  <rect x="114" y="11" width="40" height="20" rx="6" fill="#FACC15" stroke="#EAB308" stroke-width="1"/>
  <text x="134" y="24.5" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif" font-size="10.5" font-weight="800" fill="#18181B" letter-spacing="0.05em" text-anchor="middle">GPT</text>
</svg>
"""

# Minified single-line SVG templates to prevent Markdown indentation parsing
LOGO_MARK_SVG = " ".join(line.strip() for line in _LOGO_MARK_RAW.splitlines() if line.strip())
LOGO_FULL_SVG = " ".join(line.strip() for line in _LOGO_FULL_RAW.splitlines() if line.strip())

# Cohesive 2px round-stroke vector icon set
ICONS = {
    "create": '<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "history": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "sparkles": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>',
    "trash": '<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    "copy": '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    "info": '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
    "terminal": '<polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "refresh": '<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>',
    "sliders": '<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
}


def render_logo_mark_svg(size: int = 34) -> str:
    """Return inline SVG for the standalone sunlit geometric logo mark."""
    return LOGO_MARK_SVG.format(size=size)


def render_full_logo_svg(
    height: int = 38,
    dark_mode: bool = False,
) -> str:
    """Return inline SVG for the full ExcuseGPT logo with mark and wordmark."""
    width = int(height * (210 / 40))
    text_color = "#FAF9F5" if dark_mode else "#18181B"
    return LOGO_FULL_SVG.format(
        width=width,
        height=height,
        text_color=text_color,
    )


def render_icon_svg(name: str, size: int = 16, color: str = "currentColor") -> str:
    """Return an inline vector SVG icon from the unified ExcuseGPT icon library."""
    path = ICONS.get(name, ICONS["info"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align: -0.15em; display: inline-block; flex-shrink: 0;">'
        f'{path}</svg>'
    )