# STEPS TO CONTRIBUTE TO THIS PROJECT

## Open your terminal and run the following git command:

## 1. Clone the repo
```sh
git clone https://github.com/hngx-org/Metal-food-backend.git
```
## 2. Change into the repository directory on your computer (if you are not already there):

```sh
cd Metal-food-backend
```
## 3. Create and activate a virtual environment (optional but recommended):
 On Mac
 ```sh
  python3 -m venv venv
  ```

```sh
source venv/bin/activate
```
On Windows

```sh
python -m venv venv
```
```sh
venv\Scripts\activate
```
or

```sh
.\venv\Scripts\Activate
```

## 4. Install the dependencies:

```sh
pip install -r requirements.txt
```

## 5. Create a new branch that describes the changes that you're going to make. For example, to create a branch named "fixing-bug", enter the following command:

```sh
git branch fixing-bug
```

## 6. Switch to the branch by entering `git checkout <name-of-branch>`. For our example, the command will be:

```sh
git checkout fixing-bug
```

## 7. Pull Changes from the Remote Branch(new_default):

```sh
git pull origin new_default
```

## 8. Resolve Conflicts (if any):

If there are any conflicts between your local branch and the changes you pulled from the remote branch, Git will notify you. You'll need to resolve these conflicts manually. Once resolved, add the changes, commit them, and continue with your work.


## 9. Make changes and commit the changes


## 10. Please make sure you pull Changes from the Remote Branch(new_default) once again before you push. Run this again

```sh
git pull origin new_default
```

then 

```sh
git push -u origin <Your-branch>
```

## 11. Submit your changes for review

Go to the project repo on GitHub, Click on the `Compare & pull request` button.
THIS TIME, PLEASE COMPARE AND SEND PR TO NEW_DEFAULT BRANCH, ONCE PR IS SENT, PLEASE STANDBY AND WAIT FOR REVIEW. DON'T MERGE YOURSELF.YOU WILL GET A NOTIFICATION EMAIL ONCE THE CHANGES HAVE BEEN MERGED. THANKS...
