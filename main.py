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
PROJECT_FILE = "monitor_flipflop.dbpr"

# Load the project file AFTER importing
projFile = r1.ProjectFile(PROJECT_FILE)

try:
    # Clean up existing AutoR1 data
    autor1.clean(projFile)

    # Create Show Page View only
    autor1.create_show_page(projFile)

    print(f"✅ Finished processing project: {PROJECT_FILE}")

except Exception as e:
    print(f"❌ Error during project processing: {str(e)}")

projFile.close()
print("🔄 Closed project file and database connection.")