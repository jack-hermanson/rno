import os

from application import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5040"))
    app.run(debug=True, port=port)
