echo "Running mypy..."
uv run mypy .

echo
echo "Running ruff checker..."
uvx ruff check

echo
echo "Running ruff formatter..."
uvx ruff format
