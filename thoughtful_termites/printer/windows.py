import win32print


def listener():
    saved_pages = 0
    passed = []

    while True:
        # List out every print job from every printer
        # TODO: Add an option to exclude certain printers that don't physically print paper
        for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
            flag, desc, name, comment = p
            phandle = win32print.OpenPrinter(name)

            jobs = list(win32print.EnumJobs(phandle, 0, -1, 1))
            printing = [x for x in jobs if x["Status"] == 0]

            # Remove all print jobs in `passed` that don't exist in the
            # print queue anymore
            for tup in passed:
                ph, job_id = tup
                ids = [x["JobId"] for x in jobs]

                if ph == phandle and job_id not in ids:
                    del tup

            # Fetch all the print jobs that the user has "passed", i.e.
            # jobs that they want to print after being prompted
            passed_phandle = [x[1] for x in passed if x[0] == phandle]

            # Prompt the user for each print job
            for job in printing:
                if job["JobId"] in passed_phandle:
                    continue

                win32print.SetJob(phandle, job["JobId"], 1, job, win32print.JOB_CONTROL_PAUSE)
                will_cancel = input("Do you wish to cancel this print job? (y/n) >>> ")
                print(will_cancel)

                if will_cancel == "y":
                    pages = job["TotalPages"]
                    saved_pages += pages

                    print(f"Pages cancelled: {pages}, total pages saved: {saved_pages}")

                    win32print.SetJob(phandle, job["JobId"], 0, None, win32print.JOB_CONTROL_DELETE)
                elif will_cancel == "n":
                    win32print.SetJob(phandle, job["JobId"], 1, job, win32print.JOB_CONTROL_RESUME)
                    passed.append((phandle, job["JobId"]))

            win32print.ClosePrinter(phandle)
