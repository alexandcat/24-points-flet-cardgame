![Screenshot of 24‑points card renderer](assets/screenshot.png)

# Twenty-Four Card Renderer

A Flet-based 24-point playing card face renderer that supports standard suit layouts for ranks 1-10, corner rank markers, and suit symbol rendering.

## Features

- Standard card face: ranks 1~10 (1 displayed as "A")
- Runs in the browser; click the button to deal 4 random cards

## Running

```bash
pip install flet
python twentyfour_card_render.py
```

## Reference Project

This project references the card face design of [52CardEngine](https://github.com/Xerako/52CardEngine/tree/main) (by Xerako):

- The card color scheme is taken from 52CardEngine's `settings.py`
- Fixed the mismatch between card pips and card ranks, and optimized the rendering effects

## License

MIT

