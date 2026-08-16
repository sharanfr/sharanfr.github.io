# r.sreesaran — personal portfolio

Minimalist portfolio site built with vanilla HTML, CSS, and JS.  
Deployed on GitHub Pages → [sharanfr.github.io](https://sharanfr.github.io)

---

## stack

- **HTML / CSS / JS** — no frameworks, no build step
- **Bootstrap Icons** — via CDN, themed with `currentColor`
- **Google Fonts** — Space Grotesk + JetBrains Mono
- **GitHub Pages** — static hosting

## structure

```
website/
├── index.html              # entry point
├── favicon.svg             # adaptive SVG favicon (light/dark)
├── assets/
│   ├── css/
│   │   └── style.css       # all styles + theme variables
│   ├── js/
│   │   └── main.js         # theme system, clock, cursor, typewriter
│   └── images/
│       └── og-image.png    # social preview card (1200×630)
└── tools/
    └── qr_gen.py           # QR code generator (4 color themes)
```

## themes

| theme    | background | accent     |
|----------|-----------|------------|
| `ink`    | white     | `#CC0000` red |
| `void`   | black     | `#F0F0F0` white |
| `signal` | black     | `#FF3040` red |
| `paper`  | white     | `#1A1A1A` dark |

Switch themes with the dot controls in the nav, or press **`T`** to toggle dark/light.

## qr generator

```bash
cd tools
python3 qr_gen.py https://sharanfr.github.io
# or interactive:
python3 qr_gen.py
```

requires: `pip install "qrcode[pil]" Pillow`

---

*built with zero em dashes*
