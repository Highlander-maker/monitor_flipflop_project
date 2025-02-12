import sqlite3
import logging
import os.path

log = logging.getLogger(__name__)

class sqlDbFile:
    """Handles SQLite database operations for R1 project files."""
    def __init__(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"❌ File does not exist: {path}")

        self.path = path
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()
        log.info(f"✅ Connected to SQLite DB: {self.path}")

    def close(self):
        """Safely close the SQLite database connection."""
        try:
            self.db.commit()
        except Exception:
            pass
        self.db.close()
        log.info("🔄 Closed database connection.")

class ProjectFile(sqlDbFile):
    """Handles the R1 project file (.dbpr)."""
    def __init__(self, path):
        super().__init__(path)
        log.info(f"✅ Loaded R1 project file: {path}")

    def createGrp(self, name, parent_id):
        """Creates a group in the R1 project."""
        self.cursor.execute(
            f'INSERT INTO Groups (Name, ParentId) VALUES ("{name}", {parent_id})'
        )
        self.db.commit()
        log.info(f"✅ Created group: {name}")
        return self.getHighestGroupID()

    def deleteGroup(self, group_id):
        """Deletes a group from the R1 project."""
        self.cursor.execute(f"DELETE FROM Groups WHERE GroupId = {group_id}")
        self.db.commit()
        log.info(f"✅ Deleted group ID: {group_id}")

    def getHighestGroupID(self):
        """Finds the most recently created Group ID"""
        self.cursor.execute(f"SELECT max(GroupId) FROM Groups")
        return self.cursor.fetchone()[0]

    def getViewIdFromName(self, name):
        """Gets View ID by name."""
        self.cursor.execute(f'SELECT ViewId FROM Views WHERE Name = "{name}"')
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None