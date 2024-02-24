test-all:
  pytest tests

create-migration NAME:
  dotenv -f migrations/.env run -- dbmate new {{NAME}}

migrate:
  dotenv -f migrations/.env run -- dbmate up

rollback-migration:
  dotenv -f migrations/.env run -- dbmate down
