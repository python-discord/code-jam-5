import traceback as tb

if __name__ == '__main__':
    try:
        from thoughtful_termites import bot
        bot.run()

    except Exception:
        tb.print_exc()
        input('Press enter to exit.')
