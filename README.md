# GitHub Actions Experiments

This repository illustrates how GitHub Actions can be used to automate software development processes. GitHub Actions are scripts that run on a containerized platform hosted on GitHub. A GitHub action is defined by creating a `.yml` file in the `.github/workflows` directory of a repository (as done here). Such an action needs to be follow a specific format as described in the [GitHub documentation](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions). An example is provided in  the `triage_issues.yml` action file:

```yaml
name: "Label Issues for Triage"
on:
  issues:
    types:
      - reopened
      - opened
jobs:
  label_issues:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - run: gh issue edit "$NUMBER" --add-label "$LABELS"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_REPO: ${{ github.repository }}
          NUMBER: ${{ github.event.issue.number }}
          LABELS: triage
```

An action consists of the following basic components:
- `name`: name of the action.
- `events`: the `on` keyword specifies under what circumstance the action should run. In this example, the action will run when an issue is opened or reopened.
- `jobs`: specifies one or more things that should happen when the event is triggered. Here, we issue a command to GitHub to edit the modified issue by adding a label.

We will see other types of events and actions later on.

If you are familiar with **containerized applications**, you will notice familiar concepts. One key aspect of a container is to specify its base operating system. Here, we specify that we want to run the latest available version of Ubuntu, which is a Linux operating system. Jobs are similar to `RUN` commands in Docker but are tailored specifically to the task of automating processes and provide many capabilities related to interacting with GitHub.

Now that you understand the basic structure of a GitHub Action, we will see on in, well, action.

## Exercise 1 - Issue Action

In this exercise, we will run our first GitHub Action It is already defined so you don't have to do too much to see it execute and the result of its execution.

Let's assume we have developed an application that is open source and is wildly popular with developers. As developers use your application, they also find bugs and ways to improve the application. When they do, they usually submit a GitHub issue. We need a way of making sure that we triage all the new issues appropriately. In this exercise, we will work with a GitHub Action that automatically tags all new issues that are submitted with the label `triage`.

To see the it in action, simply create a new issue with any title. Stay on the page and wait until the label `triage` magically appears. When it does, you know the GitHub Action did it's job.

You can also view every run of a GitHub Action by clicking on `Actions` in the repository toolbar. The green checkmark indicates that the run was successful. Clicking on the job name, tells you more about that particular run. On the next page, click on the box that indicates the job that was executed as part of that action. Now you see all the details of the run.

## Exercise 2 - Smarter Issue Labeling

We have already seen an example of labeling issues automatically for triage. However, we might want GitHub Actions to perform smarter tagging by recognizing what type of issue the user submitted. We can implement it from scratch or we can use an [existing library](https://github.com/damccorm/tag-ur-it) to do most of the work for us. The repository description for [`tag-ur-it`](https://github.com/damccorm/tag-ur-it) describes how to set up and configure custom labeling.

Create a new file `.github/workflows/autotag.yaml` and copy in the following content:

```yaml
name: "Auto Tag"
on:
  issues:
    types: [opened, edited]

permissions:
  issues: write
  contents: read

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
    - uses: damccorm/tag-ur-it@master
      with:
        repo-token: "${{ secrets.GITHUB_TOKEN }}"
        configuration-path: "issue-rules.yml"
```

The GitHub Action specified above is very simple: it executed when an issue is opened or re-opened. It then checks out your repository code and runs the [`tag-ur-it`](https://github.com/damccorm/tag-ur-it) job. It can do more than just label issues. The behavior is configured in `config/issue-rules.yml`. Note that the file specifies that if the term `enpm611` appears in the issue text, the issue is assigned to the GitHub user `enpm611`:

```yaml
rules:
...
- contains: enpm611
  assign: ['enpm611']
```

After you created that file, push your changes to the repository. Then, work on the following tasks:

* **Task A**: create a new rule that assigns the label `question` if the issue contains the term `maybe`.

* **Task B**: add a rule that assigns the issue to your user if the issue contains the term `urgent`.


## Exercise 3 - Continuous Integration

Continuous Integration (CI) relies heavily on automating processes so that we an focus on development and let tools take care of giving us feedback when something goes wrong. Hence, a core part of CI is to automated the running of tests whenever someone pushes code to the repository. The goal is to get immediate feedback telling us that whether what we commited is of acceptable quality.

Now, you will create a new GitHub Action. First, in the folder `.github/workflows`, create a file named `autotest.yml`. Then, copy and paste the following YAML specification into the file and save it:

```yaml
name: "Continuous Integration"

on: push

jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12.4'
      
      - name: Install Dependencies
        run: 
          pip install -r requirements.txt

      - name: Run Tests
        run: pytest
```

This action is executed whenever someone does a `push`. It will perform several `steps` as part of the `test` job. First, it checks out the source code from your repository. We are using a pre-defined [checkout action](https://github.com/actions/checkout) for this. You can see that we can reuse actions also! Then, we set up a Python environment so that we can run our code using the [setup-python action](https://github.com/actions/setup-python). As you know, we can't execute our Python code if we don't first install our dependencies. So next, we are doing exactly that by running the `pip install` command. Finally, we can run our tests by running `pytest`. This will run all the test defined in this repository and let us know if the tests pass. 

After you created the file and copied the action above, push the change to the repository. Next, work on the following tasks:

* **Task C**: Add a test case to either test file and push your changes to your repository. Check the run of the action to see what status is finishes with. 

* **Task D**: You will notice that the action shows a red x after it has completed its run. Investigate why that action failed. Resolve the issue and push to the repository to trigger the action again.




Task 1

Automated testing on commit

a) Create a new branch called `test` and push it to the repository. Then create a PR for that branch.
b) Observe the test results. If there is a bug, update the test case to match the value that is returned by the function.
c) Push the updated code. Observe the test results.



Task 2

Add release notes to README

a) Create a new branch called `release` and push it to the repository. 
b) Then create a PR for that branch and add a bulleted list of changes.
b) Check that the release notes are added to the `README.md` file.


Task 3

Deploy on merge

a) Create a new branch called `deploy1` and push it to the repository. Then create a PR for that branch.
b) Merge the PR into `main`.
c) Navigate to the deployed app
d) Change the app title and create a new PR. Merge the PR into `main`. Navigate to the deployed app again.Observe the changes.

# Release Notes

