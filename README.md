# *API* для благотворительного фонда *QRkot_spreadseets*

## Описание
Фонд собирает пожертвования на различные целевые проекты. С помощью *API* можно создавать целевые проекты с названием, описанием и целевой суммой. Пожертвования направляются в первый открытый проект и когда он закрывается, переходят к следующему по принципу `First In, First Out`. Синхронизированно с Google spreadseets (гугл-таблицей).
В таблице будут все закрытые проекты, отсортированные по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.
## Технологии
- `Python 3.10.10`
- `FastAPI`
- `FastAPI-users`
- `SQLAlchemy`
- `Pydantic`
- `Asyncio`
- `Aiogoogle`
## Установка
1. Клонируйте проект 
```BASH
git clone https://github.com/yonvik/QRkot_spreadsheets.git
```
2. Перейдите в корневую директорию проекта 
```BASH
cd cat_charity_fund/
```
3. Установите виртуальное окружение с `Python 3.10.10` и активируйте его  
4. Далее установите зависимости 
```BASH
pip install -r requirements.txt
```
5. Заполните `.env` по образцу:
```BASH
APP_TITLE=Благотворительный фонд поддержки котиков QRKot.
APP_DESCRIPTION=Фонд сбора средств, направленные на помощь котиков.
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SECRET_WORD
SUPERUSER_EMAIL=perfectuser@memail.ru
SUPERUSER_PASSWORD=perfectuser
TYPE=service_account
PROJECT_ID=your_projectid
PRIVATE_KEY_ID=your_private_key
PRIVATE_KEY=-----BEGIN PRIVATE KEY-----your_private_key-----END PRIVATE KEY-----
CLIENT_EMAIL=client@your_projectid.iam.gserviceaccount.com
CLIENT_ID=123456789012345678901
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/client%40your_projectid=.iam.gserviceaccount.com
EMAIL=your@gmail.com
```   
6. Примините миграции
```BASH
alembic upgrade head
```
7. Запуск проекта. Можно добавить флаг `--reload`, тогда при изменении файлов приложение будет перезапускаться
```BASH
uvicorn app.main:app
```
## Примеры запросов
После развёртывания проекта документацию можно найти на эндпоинте `.../docs/`
### Благотворительные проекты
POST-запрос .../charity_project/:
```JSON
{
  "name": "На корм для кошек",
  "description": "Кошки хотят кушать",
  "full_amount": 2500
}
```
Ответ (200):
```JSON
{
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2023-03-13T15:11:47.980127",
  "name": "На корм для кошек",
  "description": "Кошки хотят кушать",
  "full_amount": 2500,
  "id": 10
}
```
### Пожертвования
POST-запрос .../donation/
```JSON
{
  "comment": "На корм",
  "full_amount": 125000
}
```
Ответ (200):
```JSON
{
  "comment": "На корм",
  "full_amount": 125000,
  "id": 2,
  "create_date": "2023-03-13T15:15:16.679223"
}
```
## Автор
[Янковский Андрей](https://github.com/yonvik)
