-- migrate:up
CREATE TABLE storages (
    id UUID PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL,
    owner_id UUID REFERENCES users (id) NOT NULL,
    link VARCHAR(255) NOT NULL,
    expenses_table_link VARCHAR(255) NOT NULL,
    income_table_link VARCHAR(255) NOT NULL
);

-- migrate:down
DROP TABLE storages;
