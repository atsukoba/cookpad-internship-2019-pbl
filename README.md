# ColorChef

**「一人暮らしの料理を楽しくするサービス」**

*20代社会人女性の料理と食卓を華やかに。色と写真からレシピを探せるサービス*

## install and run

```shell
bash ngrok-install.sh
```

```shell
bash run.sh
```

and access the QR code

## functions

- search Cookpad recipe images by color
- search Cookpad recipe images by image
- likes (bookmarks)

with instagram-like, easily accessible gallery UI

## api

implemented with `flask`

### endpoints

- `/` GET : top page
- `/search` GET : color code on query
- `search/photo` GET, POST
- `recipes`
- `likes` GET, PUT

recipes like data is stored on `sqlite`

## frontend

- `jquery`
- `Animate.css`
- scratched @keyframes animations
