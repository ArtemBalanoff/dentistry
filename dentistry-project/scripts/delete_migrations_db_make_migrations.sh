set -e

case "$OSTYPE" in
    msys*)    python=python ;;
    cygwin*)  python=python ;;
    *)        python=python3 ;;
esac

START_DIR="."

find "$START_DIR" -type d -name "migrations" | while read -r migrations_dir; do

    find "$migrations_dir" -maxdepth 1 -type f ! -name "__init__.py" -exec rm -f {} \;


done

$python manage.py makemigrations
$python manage.py migrate
