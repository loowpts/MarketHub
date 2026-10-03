# MarketHub

Маркетплейс на Django: пользователи открывают магазины, публикуют товары,
оформляют заказы через корзину и оставляют отзывы о товарах и магазинах.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django_5.2-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)

## Приложения

| Приложение | Что делает | URL |
|---|---|---|
| `users` | кастомная модель пользователя и профиль | `/users/` |
| `shops` | создание магазинов, список, карточка, модерация | `/shops/` |
| `products` | категории, товары, изображения товаров | `/products/` |
| `orders` | корзина и заказы | `/orders/` |
| `reviews` | отзывы о товарах и магазинах | `/reviews/` |

## Запуск

```bash
git clone https://github.com/loowpts/MarketHub.git
cd MarketHub
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Создать `.env` в корне проекта:

```env
SECRET_KEY=change-me
DB_NAME=markethub
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000, админка: http://127.0.0.1:8000/admin/.

## Планы

- платёжная система
- чат покупателя с магазином при оформлении заказа
- доработка интерфейса

## Лицензия

[MIT](LICENSE.md)
