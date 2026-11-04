# mlplay.app

The MLPlay website, served by GitHub Pages at https://mlplay.app.

`cagecraft/privacy.md` is copied from `docs/privacy_policy.md` in the Cagecraft repo, without its leading comment; change it there first.

`index.html` is a standalone landing page (no front matter, so Jekyll copies it as is and the theme does not apply). Its images in `assets/cagecraft/` are downscaled JPEGs of the Play store graphics in the Cagecraft repo (`assets/brand/play_store/`); redo them when those change. The page loads nothing from other sites, so it needs no cookie notice.

`brand/` holds the MLPlay developer page graphics for Google Play (`developer_icon.png`, `developer_header.jpg`). Redraw them with `uv run --with pillow python brand/make_brand.py`. Jekyll does not publish the folder.
