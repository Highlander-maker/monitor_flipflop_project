import sqlite3
import logging

log = logging.getLogger(__name__)

SHOW_PAGE_NAME = "Show Page"

# Amp input configurations
AMP_MODES = {
    "2-way_active": [(1, 3), (2, 4)],
    "dual_channel": [(1, 2), (3, 4)],
}

def create_show_page(proj):
    """Generates the Show Page in R1 with snapshots, mute buttons, and metering."""
    log.info("🛠 Creating Show Page")
    
    # Get or create Show Page ViewId
    proj.cursor.execute('SELECT ViewId FROM Views WHERE Name = ?', (SHOW_PAGE_NAME,))
    show_page_id = proj.cursor.fetchone()
    
    if not show_page_id:
        proj.cursor.execute('INSERT INTO Views (Type, Name, Flags) VALUES (1000, ?, 4)', (SHOW_PAGE_NAME,))
        proj.db.commit()
        show_page_id = proj.cursor.lastrowid
        log.info(f"✅ Created Show Page (ViewId: {show_page_id})")
    else:
        show_page_id = show_page_id[0]
        log.info(f"✅ Found existing Show Page (ViewId: {show_page_id})")
    
    # Detect amplifier channels for muting & metering
    proj.cursor.execute("SELECT Name FROM Groups WHERE Name LIKE '%Stage Wedges%'")
    stage_wedges = [row[0] for row in proj.cursor.fetchall()]
    log.info(f"✅ Detected {len(stage_wedges)} stage wedges: {stage_wedges}")
    
    controls = []
    
    # Add Console A & B snapshot buttons
    controls.append((4, 50, 50, "Console A", "Snapshot_Input_A"))
    controls.append((4, 300, 50, "Console B", "Snapshot_Input_B"))
    
    # Add Mute buttons & Meters for each wedge
    pos_y = 150
    for i, wedge in enumerate(stage_wedges, start=1):
        controls.append((4, 50, pos_y, f"Mute {wedge}", "Config_Mute"))
        controls.append((7, 300, pos_y, f"{wedge} Gain", "Meter_Level"))
        pos_y += 100
    
    # Insert controls into Show Page
    for control_type, pos_x, pos_y, name, target in controls:
        proj.cursor.execute(
            "INSERT INTO Controls (Type, PosX, PosY, Width, Height, ViewId, DisplayName, TargetProperty) "
            "VALUES (?, ?, ?, 200, 100, ?, ?, ?)",
            (control_type, pos_x, pos_y, show_page_id, name, target)
        )
    
    proj.db.commit()
    log.info("✅ Finished inserting Show Page controls.")
    
    # Refresh UI in R1
    proj.cursor.execute("UPDATE Views SET Flags = Flags | 1 WHERE ViewId = ?", (show_page_id,))
    proj.db.commit()
    log.info("🔄 Forced UI refresh for R1.")
import logging

log = logging.getLogger(__name__)

def clean(proj):
    """Removes all AutoR1 groups, views, and controls."""
    log.info("🧹 Cleaning R1 project.")
    
    # Remove AutoR1-created groups
    proj.cursor.execute('SELECT GroupId FROM Groups WHERE Name = "AUTO"')
    group = proj.cursor.fetchone()
    
    if group:
        proj.deleteGroup(group[0])
        log.info(f"✅ Deleted AUTO Group")
    else:
        log.warning("⚠️ AUTO group not found.")

    # Remove all controls from Show Page
    proj.cursor.execute('DELETE FROM Controls WHERE ViewId = (SELECT ViewId FROM Views WHERE Name = "Show Page")')
    proj.db.commit()
    log.info("✅ Removed all Show Page controls")