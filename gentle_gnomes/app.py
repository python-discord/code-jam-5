"""Entry point for application."""
from src import create_app


app = create_app()


def main():
    """Run the flask app. Mostly for poetry script."""
    app.run()


if __name__ == '__main__':
    main()
