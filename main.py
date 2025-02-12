import sys
import os
import logging

# Ensure 'src' directory is in Python path
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)
    print(f"✅ Added {SRC_PATH} to sys.path")

# Import modules AFTER fixing sys.path
try:
    import r1py.r1py as r1
    import autor1.autor1 as autor1
    print("✅ Successfully imported r1py and autor1!")
except ModuleNotFoundError as e:
    print(f"❌ Import Error: {e}")
    print("❌ Check that your 'src' folder contains 'r1py' and 'autor1' directories with '__init__.py' files.")
    sys.exit(1)

# Logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Paths
PROJECT_FILE = "test_project.dbpr"
TEMPLATE_FILE = "templates.r2t"

# Ensure project file exists
if not os.path.exists(PROJECT_FILE):
    print(f"❌ Error: Project file '{PROJECT_FILE}' not found.")
    sys.exit(1)

print(f"📂 Loading project: {PROJECT_FILE}")
projFile = r1.ProjectFile(PROJECT_FILE)

# Ensure template file exists
if not os.path.exists(TEMPLATE_FILE):
    print(f"❌ Error: Template file '{TEMPLATE_FILE}' not found.")
    sys.exit(1)

print(f"📂 Checking template file: {TEMPLATE_FILE}")
tempFile = autor1.TemplateFile(TEMPLATE_FILE)
print(f"✅ Successfully loaded template file: {TEMPLATE_FILE}")

# Processing
print("🛠 Starting project processing...")

try:
    autor1.clean(projFile)

    projFile.pId = projFile.createGrp(autor1.PARENT_GROUP_TITLE, 1)
    autor1.createSubLRCGroups(projFile)
    autor1.getSrcGrpInfo(projFile)
    autor1.configureApChannels(projFile)

    # Create Show Page View
    autor1.createShowPageView(projFile)

    # Create other views
    autor1.createMeterView(projFile, tempFile)
    autor1.createMasterView(projFile, tempFile)
    autor1.createNavButtons(projFile, tempFile)

    print(f"✅ Finished processing project: {PROJECT_FILE}")

except Exception as e:
    print(f"❌ Error during project processing: {str(e)}")

projFile.close()
print("🔄 Closed project file and database connection.")