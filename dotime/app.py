"""Initialize application factory"""

from dotime import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
