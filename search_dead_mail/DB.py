# region import libraries
from .config import logger
import sqlite3
import re

# endregion


class DB:
    # region create tables sql lines
    drop_tables = [
        "DROP TABLE IF EXISTS code;",
        "DROP TABLE IF EXISTS mail;",
        "DROP TABLE IF EXISTS status;",
    ]
    create_tables = [
        """
            CREATE TABLE "code" (
            code TEXT NOT NULL,
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
        );
        """,
        """
            CREATE TABLE "mail" (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            code_id INTEGER NOT NULL,
            status_id INTEGER NOT NULL,
            mail TEXT,
            CONSTRAINT mail_FK FOREIGN KEY (id) REFERENCES code(id),
            CONSTRAINT mail_status_FK FOREIGN KEY (id) REFERENCES status(id)
        );
        """,
        """
            CREATE TABLE status (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            status TEXT
        );
        """,
    ]
    # endregion

    # region initialize class
    def __init__(self, path, *args, **kwargs):
        dbname = re.sub(r".*?\/|\..*", "", path)
        self.path = "databases/{}.db".format(dbname)
        try:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
            self._drop_tables()
            self._create_tables()
            self._insert_statuses()
            logger.info("Database opened.")
        except:
            logger.error("Failed to open database. Path: {}".format(self.path))

    # endregion

    # region work with sqlite database
    def _insert_statuses(self, *args, **kwargs):
        query = "INSERT INTO status(status) VALUES ('error'),('ok')"
        self.execute(query)

    def _create_tables(self, *args, **kwargs):
        for create in self.create_tables:
            self.execute(create)

    def _drop_tables(self, *args, **kwargs):
        for drop in self.drop_tables:
            self.execute(drop)

    def execute(self, query, *args, **kwargs):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            logger.error("Failed to execute sql query. Query: {}".format(query))

    def close(self, *args, **kwargs):
        self.connection.close()
        logger.info("Data saved to file: {}".format(self.path))

    # endregion
