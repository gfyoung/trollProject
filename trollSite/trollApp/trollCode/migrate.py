from sqlite3 import connect

DATABASE = "../../db.sqlite3"
MIGRATION = "migration.txt"
TABLE = "trollApp_download"

conn = connect(DATABASE)
latestId = conn.execute("SELECT COALESCE(MAX(id), 0) " +
                        "FROM {}".format(TABLE)).fetchone()[0]

target = open(MIGRATION, "r")
migrations = target.readlines()

if len(migrations) != latestId:
    print "Applying migrations to database..."

    for migration in migrations[latestId:]:
        conn.execute(migration.strip())
        conn.commit()

    print "Done!"
    
else:
    print "Database already up to date"
