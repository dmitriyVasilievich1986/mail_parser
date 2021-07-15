# region import libraries
from .config import logger
import sqlite3
import os
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
        """A class intended for working with a sqlite database.
        Creates a database, tables and adds data.

        Args:
            path (str): path to bd.
        """

        dbname = re.sub(r".*?\/|\..*", "", path)
        dbname = dbname if dbname != "" else "generic"
        self.path = "databases/{}.db".format(dbname)

        try:
            os.makedirs("databases")
        except OSError:
            pass

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
        """The method enters data into the "status" table."""

        query = "INSERT INTO status(status) VALUES ('error'),('ok')"
        self.execute(query)

    def _create_tables(self, *args, **kwargs):
        """The method creates new tables."""

        for create in self.create_tables:
            self.execute(create)

    def _drop_tables(self, *args, **kwargs):
        """The method delete tables, if thay already exists."""

        for drop in self.drop_tables:
            self.execute(drop)

    def execute(self, query, *args, **kwargs):
        """The method execute sql query."""

        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            logger.error("Failed to execute sql query. Query: {}".format(query))

    def close(self, *args, **kwargs):
        """The method close connection with db."""

        self.connection.close()
        logger.info("Data saved to file: {}".format(self.path))

    # endregion
