Your Personal Home Finance Manager

## Business
### Problem
1. Conveniently save your expenses in your own storage.
        1. For example, all your expenses are kept in an Excel file on Google Drive. To add an expense, you need to:
                1. Open Google Drive.
                2. Open the folder where the required file is located.
                3. Open the Excel file.
                4. Find the sheet where you record expenses.
                5. Scroll to the very end of the table.
                6. Enter the details of your expenses.
        2. How it works with Home Financier using a Telegram Bot.
                1. Open Telegram.
                2. Open a chat with the Home Financier bot.
                3. Press the menu button: `record expenses`.
                4. Provide the necessary details.

### Features
1. Connect your own storage.
        1. All data is stored on your side, the service does not keep it.
2. Record expenses with information about them.
        1. Expenses are saved in your storage.
                1. This gives you full control over your expenses.

## For developers
### Environment
Rename the `.env.template` file to `.env`. This file contains all necessary environment variables.

### Migrations
[dbmate](https://github.com/amacneil/dbmate) is used for database migrations. It is a CLI program that allows you to manage migrations using raw SQL. And yes, it's written in Go!

### CLI Interface
For the CLI interface, we use [just](https://github.com/casey/just), which is similar to `make` but lighter and faster.
