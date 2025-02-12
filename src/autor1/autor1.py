import sqlite3
import logging
import r1py.r1py as r1

log = logging.getLogger(__name__)

PARENT_GROUP_TITLE = "AUTO"

class TemplateFile(r1.sqlDbFile):
    """Handles template (.r2t) file parsing for R1 custom views."""
    
    def __init__(self, file_path):
        super().__init__(file_path)
        self.templates = []
        log.info(f"✅ Connected to SQLite DB: {file_path}")

        # Load all templates from the Sections table
        self.cursor.execute('SELECT * FROM "Sections" ORDER BY JoinedId ASC')
        templates = self.cursor.fetchall()
        log.info(f"✅ Found {len(templates)} templates in {file_path}")

        for temp in templates:
            log.info(f"✅ Loaded template: {temp[1]}")

def clean(proj):
    """Removes all AutoR1 groups, views, and controls."""
    log.info("🧹 Cleaning R1 project.")
    proj.cursor.execute(f'SELECT GroupId FROM Groups WHERE Name = "{PARENT_GROUP_TITLE}"')
    group = proj.cursor.fetchone()
    
    if group:
        proj.deleteGroup(group[0])
        log.info(f"✅ Deleted {PARENT_GROUP_TITLE} Group")
    else:
        log.warning(f"⚠️ {PARENT_GROUP_TITLE} group not found.")


import logging

log = logging.getLogger(__name__)

import logging

log = logging.getLogger(__name__)

def createShowPageView(proj):
    """Creates the Show Page with buttons and meters."""
    log.info("🛠 Creating Show Page View")

    # Get the existing Show Page ViewId
    proj.cursor.execute('SELECT ViewId FROM Views WHERE Name = "Show Page" ORDER BY ViewId DESC LIMIT 1')
    show_page_id = proj.cursor.fetchone()

    if show_page_id:
        show_page_id = show_page_id[0]
        log.info(f"✅ Found Show Page ViewId: {show_page_id}")
    else:
        log.error("❌ Show Page view not found!")
        return

    # Define controls to insert
    controls = [
        (4, 50, 50, "DS Wedges Mute", "Config_Mute"),
        (4, 50, 160, "US Wedges Mute", "Config_Mute"),
        (4, 50, 270, "SFs Mute", "Config_Mute"),
        (4, 50, 380, "Drum Fill Mute", "Config_Mute"),
        (4, 300, 50, "Console A", "Snapshot_Input_A"),
        (4, 550, 50, "Console B", "Snapshot_Input_B"),
        (7, 300, 160, "DS Wedges Gain", "Meter_Level"),
        (7, 300, 270, "US Wedges Gain", "Meter_Level"),
        (7, 300, 380, "SFs Gain", "Meter_Level"),
        (7, 300, 490, "Drum Fill Gain", "Meter_Level"),
        (7, 550, 160, "Console A Gain", "Meter_Level"),
        (7, 550, 270, "Console B Gain", "Meter_Level"),
    ]

    # Check existing controls
    proj.cursor.execute(f"SELECT DisplayName FROM Controls WHERE ViewId = {show_page_id}")
    existing_controls = {row[0] for row in proj.cursor.fetchall()}

    for control_type, pos_x, pos_y, name, target in controls:
        if name in existing_controls:
            log.info(f"⚠️ Skipping '{name}' (already exists)")
            continue  # Skip duplicates

        try:
            proj.cursor.execute(
                "INSERT INTO Controls (Type, PosX, PosY, Width, Height, ViewId, DisplayName, TargetProperty) "
                "VALUES (?, ?, ?, 200, 100, ?, ?, ?)",
                (control_type, pos_x, pos_y, show_page_id, name, target)
            )
            proj.db.commit()  # Commit EACH control
            log.info(f"✅ Inserted '{name}' at ({pos_x}, {pos_y}) targeting {target}")
        except Exception as e:
            log.error(f"❌ Failed to insert '{name}': {str(e)}")

    log.info("✅ Finished inserting controls into Show Page.")

    # **Force R1 to recognize the changes**
    proj.cursor.execute("UPDATE Views SET Flags = Flags | 1 WHERE ViewId = ?", (show_page_id,))
    proj.db.commit()
    log.info("🔄 Forced UI refresh for R1.")


def getSrcGrpInfo(proj):
    """Retrieves Source Group Info."""
    log.info("🛠 Retrieving Source Group Info")

    proj.cursor.execute("SELECT Name, SourceGroupId FROM SourceGroups")
    groups = proj.cursor.fetchall()

    if not groups:
        log.warning("⚠️ No source groups found in the project.")
        return

    for group in groups:
        log.info(f"✅ Found Source Group: {group[0]} (ID: {group[1]})")

    log.info("✅ Retrieved Source Group Info")

def createMeterView(proj, templates):
    """Creates a Meter View."""
    log.info("🛠 Creating Meter View")

    proj.cursor.execute(
        'INSERT INTO Views("Type", "Name", "Icon", "Flags") VALUES (1000, "AUTO - Meters", NULL, 4)'
    )
    proj.db.commit()

    log.info("✅ Created Meter View")

def createMasterView(proj, templates):
    """Creates the Master View in R1."""
    log.info("🛠 Creating Master View.")

    # Prevent duplicate views
    proj.cursor.execute('SELECT ViewId FROM Views WHERE Name = "AUTO - Master" ORDER BY ViewId DESC LIMIT 1')
    master_view_id = proj.cursor.fetchone()

    if master_view_id:
        master_view_id = master_view_id[0]
        log.info(f"✅ Found existing AUTO - Master ViewId: {master_view_id}")
    else:
        proj.cursor.execute(
            'INSERT INTO Views("Type", "Name", "Icon", "Flags") VALUES (1000, "AUTO - Master", NULL, 4)'
        )
        proj.db.commit()
        master_view_id = proj.cursor.lastrowid
        log.info(f"✅ Created AUTO - Master ViewId: {master_view_id}")

    # Insert Master View elements (example button)
    proj.cursor.execute(
        'INSERT INTO Controls ("Type", "PosX", "PosY", "Width", "Height", "ViewId", "DisplayName", "TargetProperty") '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (4, 100, 100, 200, 100, master_view_id, "Master Control", "Config_Mute")
    )

    proj.db.commit()
    log.info("✅ Finished inserting Master View controls.")

def createNavButtons(proj, templates):
    """Creates navigation buttons."""
    log.info("🛠 Creating Navigation Buttons")

    proj.cursor.execute(
        'INSERT INTO Controls("Type", "ViewId", "DisplayName") VALUES (12, (SELECT ViewId FROM Views WHERE Name="AUTO - Master"), "Nav Button")'
    )
    proj.db.commit()

    log.info("✅ Created Navigation Buttons")
    
    import logging

log = logging.getLogger(__name__)

def createSubLRCGroups(proj):
    """Creates L, R, and C Sub Groups in the R1 project."""
    log.info("🛠 Creating Sub LRC Groups")

    # Define subgroups
    sub_groups = [
        ("Left", proj.pId),
        ("Right", proj.pId),
        ("Center", proj.pId),
    ]

    # Insert groups
    for name, parent_id in sub_groups:
        try:
            proj.cursor.execute(
                f'INSERT INTO Groups ("Name", "ParentId") VALUES ("{name}", {parent_id})'
            )
            log.info(f"✅ Created Sub Group: {name} under ParentId {parent_id}")
        except Exception as e:
            log.error(f"❌ Failed to create subgroup '{name}': {str(e)}")

    proj.db.commit()
    log.info("✅ Finished creating Sub LRC Groups.")
    
    import logging

log = logging.getLogger(__name__)

def configureApChannels(proj):
    """Configures the ArrayProcessing (AP) channels in R1."""
    log.info("🛠 Configuring AP Channels")

    # Define AP channels
    ap_channels = [
        ("DS Wedges", "Config_AP_Channel"),
        ("US Wedges", "Config_AP_Channel"),
        ("SFs Tops", "Config_AP_Channel"),
        ("SFs Subs", "Config_AP_Channel"),
        ("Drum Fill", "Config_AP_Channel"),
    ]

    # Insert into Controls table
    for name, target in ap_channels:
        try:
            proj.cursor.execute(
                f'INSERT INTO Controls ("Type", "PosX", "PosY", "Width", "Height", "ViewId", "DisplayName", "TargetProperty") '
                f'VALUES (3, 50, 50, 200, 100, (SELECT ViewId FROM Views WHERE Name = "Show Page" LIMIT 1), "{name}", "{target}")'
            )
            log.info(f"✅ Configured AP Channel '{name}' targeting {target}")
        except Exception as e:
            log.error(f"❌ Failed to configure '{name}': {str(e)}")

    proj.db.commit()
    log.info("✅ Finished configuring AP Channels.")