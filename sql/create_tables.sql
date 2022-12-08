--create types
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'calculations_status') THEN
        CREATE TYPE calculations_status AS ENUM ('queued', 'processing', 'complete');
    END IF;
END$$;

-- create tables
CREATE TABLE IF NOT EXISTS calculation_tasks (
  id SERIAL PRIMARY KEY,
  status calculations_status NOT NULL DEFAULT 'queued',
  calc_start TIMESTAMP,
  calc_fin TIMESTAMP,
  date_start DATE,
  date_fin DATE,
  lag INT
);

CREATE TABLE IF NOT EXISTS calculation_results (
  id SERIAL PRIMARY KEY,
  task_id INT REFERENCES calculation_tasks(id),
  date DATE,
  liquid REAL,
  oil REAL,
  water REAL,
  wct REAL
);
