from api.utlils import get_preferences
from api.logic import get_matching
import sqlite3

# Connect to the database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Remove all rows from the final_matching table
cursor.execute("DELETE FROM final_matching")

# Fetch all rows from the final_matching table to verify
cursor.execute("SELECT * FROM final_matching")
rows = cursor.fetchall()

# Print the rows
print("Rows after deletion:")
print(rows)

# Commit the changes and close the connection
conn.commit()
conn.close()
