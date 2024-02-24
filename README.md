# HomeFinancier
Твой собственный домашний финансист

## Business
### Problem
1. Удобное сохранение твоих трат в твое хранилище.
	1. Например все твои траты содержаться в excel в Google Drive. Чтобы добавить одну трату, тебе нужно сделать следующее:
		1. Открыть Google Drive.
		2. Открыть папку в которой находится нужный тебе файл.
		3. Открыть этот Excel файл.
		4. Найти страницу в которой ты указываешь траты.
		5. Пролистать в самый конец таблицы.
		6. Добавить данные о твоих тратах.
	2. Как это происходит с Home Financier, используя Telegram Bot.
		1. Открыть Telegram.
		2. Открыть чат с ботом Home Financier.
		3. Нажать кнопку в меню: `внести траты`.
		4. Указать необходимые данныe.

### Features
1. Подключение твоего хранилища.
	1. Все данные хранятся у тебя, сервис не хранит их у себя.
2. Внесение трат с информацией о них.
	1. Траты сохраняются в твое хранилище.
		1. Дает тебе возможность иметь полный контроль над твоими тратами.


## Documentation
### Migrations
[dbmate](https://github.com/amacneil/dbmate) is used for migrations. It is CLI program that gives you an ability to manage migration using raw SQL. And, heh, written in GO :)


## CLI interface
[just](https://github.com/casey/just) is used for CLI interface. It is like a `make`, but lighter and faster.
