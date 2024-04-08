test-all:
  pytest tests

create-migration NAME:
  dotenv -f envs/dev.env run -- dbmate new {{NAME}}

migrate:
  dotenv -f envs/dev.env run -- dbmate up

rollback-migration:
  dotenv -f envs/dev.env run -- dbmate down

up-test-env:
  dotenv -f envs/test.env run -- dbmate up

drop-test-env:
  dotenv -f envs/test.env run -- dbmate drop
