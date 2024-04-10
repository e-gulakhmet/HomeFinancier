# Home Financier - Your Personal Home Finance Manager

## Introduction
Home Financier is a personal finance management tool designed to simplify the way you track and manage your expenses and income. With a focus on privacy and user control, Home Financier allows you to connect your own storage solutions, such as Google Sheets, to record and analyze your financial data.

## Features
- **Own Your Data**: All financial data is stored in your personal storage, ensuring full control and privacy.
- **Expense Tracking**: Easily record your expenses with detailed information, including categories, amounts, and dates.
- **Income Recording**: Keep track of your income sources and amounts in a structured manner.
- **gRPC API**: A robust gRPC API for seamless integration with other services.
- **Google Sheets Integration**: Leverage the power of Google Sheets for storage and advanced data manipulation.
- **Secure Authentication**: Protect your financial data with robust authentication mechanisms.

## Quick Start
To get started with Home Financier, follow these simple steps:
1. Clone the repository to your local machine.
2. Install the required dependencies using Poetry.
3. Set up your environment variables based on the `.env.template`.
4. Initialize the database and apply migrations.
5. Start the server using the provided Makefile commands.

## Prerequisites
Before setting up Home Financier, ensure you have the following installed:
- Python 3.12 or higher
- Poetry package manager
- Docker and Docker Compose (for containerized environments)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/homefinancier.git
   ```
2. Navigate to the project directory:
   ```bash
   cd homefinancier
   ```
3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
4. Copy the environment template and configure the variables:
   ```bash
   cp .env.local .env
   ```
5. Run database migrations:
   ```bash
   make migrate
   ```

## Usage
To start the Home Financier server, run:
```bash
make serve
```
Access the application through your web browser or interact with the Telegram bot to manage your finances.

## Testing
To ensure the quality and stability of the application, run the test suite with:
```bash
make test-all
```

## Docker
For containerized environments, use the provided Docker Compose configuration to deploy Home Financier:
1. Copy the environment template and configure the variables:
```bash
cp .env.docker .env
```
2. Run `docker-compose`:
```bash
docker-compose -f deployment/docker-compose.yaml up --build
```
