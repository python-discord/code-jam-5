# Python Discord Code Jam 5: It's getting hot in here!
Welcome to the fifth Python Discord code-jam!

Your theme for this code jam is **climate change**.

Because this is a free-for-all, you are free to make anything you want, as long as it fits this theme. We'd love if you created something that might help raise awareness, but first and foremost, we want you to create something _fun_.

# Getting Started
1. Have your leader fork this repo. If your leader is unavailable, it's okay that someone else does it.
2. All team members should git clone the fork.
3. **IMPORTANT: Change the folder name inside the repo from `YOUR_TEAM_NAME` to your actual teamname, e.g. `solar_seals`.**
4. Now that you've changed the folder name, you can open a pull request from your fork's `master` branch to this repo's `master`.
5. Because you are making your pull request from `master`, it would be in your best interest to work on your project inside of other branches, and then periodically merge those branches into your `master` branch. For an ideal developer workflow, you should probably be opening pull requests inside your fork, targeting your own `master` branch. If this doesn't make any sense to you because you're not that well-versed in git, you will probably be okay with all of you just pushing code directly to your master branch, but keep in mind that this may lead to conflicts if you are all working in parallel.
6. The Pull Request will be automatically updated whenever you push code to `master` on your fork, so all you have to do is keep pushing code to it and make sure you are finished before the code jam ends!

# Important considerations
- You **must** write documentation. There is a README.md file inside of the `YOUR_TEAM_NAME` folder which we expect you to fill with everything we need in order to test your software. Failure to provide this may lead to being docked points, or in extreme cases, disqualification.
- All Pull Requests made to this repo will automatically be **linted**. If the build fails, we will not be able to merge your pull request. This means, we expect you to submit code that has code style which is in accordance with PEP8. Specifically, we need you to use a tool called `flake8` in order to lint the code. We have provided a `.flake8` file in your team folder which contains certain exceptions and stuff like acceptable linelength, and `flake8` will automatically use this when linting.
- If you wish to use `black` to automatically reformat your code to be PEP8 compliant, that is absolutely fine, but be aware that we make no guarantees that code that's been run through black will pass our `flake8` lint, so it's up to you to double check that.
- You may use any third party module that's available on PyPI, but you should then provide a `requirements.txt`, a `Pipfile` or some other form of dependency management list so that we can easily install these.
- Absolutely all code should be inside of your team folder, not in the root level. This is to ensure we can merge your pull requests into this repo when the jam is over, which gives you GitHub contribution credit towards our organisation.

# Documentation

We've written a couple of documents that may help you get started with the codejam:

- If you've never used git before, check out the [How to use git](https://github.com/python-discord/code-jam-5/wiki/How-to-use-git) in the repository wiki.

- For information on how to correctly fork the repository and how to create a Pull Request, see [Opening a pull request](https://github.com/python-discord/code-jam-5/wiki/Opening-a-Pull-Request)

- If you're curious about how we judge code jam submissions, take a look at the [How does judging work?](https://github.com/python-discord/code-jam-5/wiki/How-does-judging-work%3F).

# Rules

1. The majority of your project must be Python
    - Web projects are permitted but it is important you do most of your work in Python
2. Should you opt for a GUI based project all your logic and rendering of graphics must be performed in Python
3. Your solution should ideally be cross-platform and include detailed guides for installing any dependencies
4. Your project must be feasible to run and simple to set up.
5. You must get contributions from every member of your team, if you have an issue with someone on your team please contact a member of the administration team.
6. Your development must take place on GitHub
7. All code submitted must be written within the bounds of the jam
    - Late commits may be discounted, make sure you leave enough time to bug test your program
8. This jam we have not put a restriction on the type of project
    - Make sure to pick something that all members of your team are comfortable with
    - You only have 9 days to work on your project, don't pick something that you won't be able to complete in time.
    - Please pick something that it will be feasible for us to demonstrate live on the judging stream.

