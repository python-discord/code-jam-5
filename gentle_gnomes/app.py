"""Entry point for application."""
from src import create_app


app = create_app()


def main():
    """
    Run the flask app. Mostly to play nice with poetry.
    """
    app.run()


if __name__ == '__main__':
    main()
