set -e

case "$OSTYPE" in
    msys*)    python=python ;;
    cygwin*)  python=python ;;
    *)        python=python3 ;;
esac

START_DIR="dentistry-project/"

find "$START_DIR" -type d -name "migrations" | while read -r migrations_dir; do

    find "$migrations_dir" -maxdepth 1 -type f ! -name "__init__.py" -exec rm -f {} \;


done

cd dentistry-project
rm -f "db.sqlite3"
$python manage.py makemigrations
