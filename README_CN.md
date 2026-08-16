![Screenshot of 24‑points card renderer](assets/screenshot.png)

# 24点纸牌渲染器 (Twenty-Four Card Renderer)

基于 Flet 的 24 点纸牌牌面渲染器，支持 1-10 点数的标准花色排列、角落点数标记与花色符号渲染。

## 功能

- 标准纸牌牌面：1~10 点数（1 显示为 "A"）
- 网页端运行，点击按钮随机发 4 张牌

## 运行

```bash
pip install flet
python twentyfour_card_render.py
```

## 参考项目

本项目参考了 [52CardEngine](https://github.com/Xerako/52CardEngine/tree/main)（作者 Xerako）的牌面设计：

- 牌面配色方案取自 52CardEngine 的 `settings.py`
- 修正了牌面花色和牌面数字不符的错误，以及优化了渲染效果


## License

MIT
