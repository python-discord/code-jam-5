# untitled-ultrasonic-unicorn
A placeholder for the ultrasonic unicorn project

This is a living document.  Feel free to make any corrections or additions you 
think would be helpful.

[github_page]: https://github.com/PseudoDesign/code-jam-5
[repository]: https://github.com/PseudoDesign/code-jam-5.git

## Development Environment Setup

### Install Required Software

* Download and install [Python 3.7](https://www.python.org/downloads/)
* Download and install a recent version of [PyCharm](https://www.jetbrains.com/pycharm/download)
* Download and install [git](https://git-scm.com/downloads)

### PyCharm Setup

#### Clone the Repository

* From the PyCharm menu bar, select `VCS->Checkout from Version Control->git`:

![](images/git-checkout.png)

* Click `Log in to GitHub...` and provide your login information

* Paste the link to the repository:
 `https://github.com/PseudoDesign/code-jam-5.git` and select `Clone`

![](images/clone.png)

#### Open the project subdirectory
We need to work from a subdirectory with our project files.  Open the `ultrasonic_unicorns`
subdirectory in PyCharm.

#### Pipenv Setup

Follow the instructions provided on [PyCharm's website](https://www.jetbrains.com/help/pycharm/pipenv.html).
The Pipfile already exists for this project.

#### Verify Development Environment

The most straightfoward way to make sure your environment is set up correctly is to run the unit tests.

Right-click the "tests" directory, and select `Run Unittests in tests`:

![](images/run-tests.png)


## Development Practices

### Work Tracking

We're using a [Trello board](https://trello.com/b/7Ps4Girs/codejam-summer-2019) to track work for this project

### Unit Tests

"*Untested Code is Broken Code*" - Alan Turing (Probably)

Bugs happen, and tests are a great way to catch them before they turn 
into embarrassing demos.  [Test Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
is a software development practice where (in general) developers write tests for
their software before writing the software itself.

Python's [unittest](https://www.geeksforgeeks.org/unit-testing-python-unittest/) 
library is well suited for Test Driven Development.  Unit testing can be challenging;
if you haven't developed this way before, expect to learn a lot of lessons along the way.


### Version Control

Git and GitHub have great interfaces for managing branches and pull requests.

#### Managing Git Branches

Any work done for the project should be done in a git branch to allow the team to easily review your changes.

PyCharm has great [branch support](https://www.jetbrains.com/help/pycharm/manage-branches.html), 
or you can simply use the command line to manage your branches.  

#### Comitting Changes to the Repository

Once you've pushed your branch to the repository, you can open a pull request on
the project's [GitHub Page][github_page].  This will allow the rest of the team to
review code and ensure that the unit tests are passing before committing it to the master branch.