import traceback as tb

if __name__ == '__main__':
    try:
        import thoughtful_termites.bot
    except Exception:
        tb.print_exc()
        input('Press enter to exit.')
