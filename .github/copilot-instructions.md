## SQLite Databse Usage Rules

- SQLite connection are merged in `api/repository/init_db.py`.
- Pass the `db` connecion object as an argument to repository layer functions.
- Do not call `db.close()` in the repository layer.
- The service layer is responsible for opening/closing the databse and managin transactions (e.g., `commit`, `rollback`).
