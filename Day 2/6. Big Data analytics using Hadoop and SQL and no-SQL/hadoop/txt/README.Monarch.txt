This describes the development environment and process followed for 
Windows porting development.

--------------------------------------------------------------
Git repository for development based on Apache branch-1-win
--------------------------------------------------------------
Step 1: Get access to git repo 
https://github.com/hortonworks/hadoop-monarch
used for development.

Step 2: Setup your git project. Checkout the branch-1-win branch 
 from github.
1. git clone https://github.com/hortonworks/hadoop-monarch hadoop-monarch
2. git checkout -B branch-1-win origin/branch-1-win   // To checkout the branch

Step 3: Setup apache as the upstream project
# git remote add apache git://git.apache.org/hadoop-common.git
# git fetch apache 
# git remote -v // shows newly added remote repositories

Step 4: Doing development (Before doing this, understanding basic 
Git stuff is a good idea)
1. Make the changes in your area
2. git add <new files/modified files> (To stage your changes by doing)
3. git commit (To commit your changes)
4. git push origin branch-1-win (Push the commit to github)

Step 5: Watching the project and tracking the changes in the project
See the link on how to watch the project: http://help.github.com/be-social/

--------------------------------------------------------------
Some useful tips:
--------------------------------------------------------------
1. To look at all the remote branches
# git remote -r  
Shows all the branches including the newly added remote repo apache

2. Merging a change from apache branch to github branch
# Find the commit id for a commit using command git log
# git cherry-pick commitid (e.g. git cherry-pick 1ec58718f53b9cd355b71c22b706e9f66789db77)
# Resolve any conflict
# git commit
# git push

3. Checking out the diff between your github branch and apache
git diff <remote-branch> (e.g. git diff apache/branch-1-win)


--------------------------------------------------------------
Some useful links:
--------------------------------------------------------------
Useful links for git:
http://help.github.com/fork-a-repo/
http://help.github.com/remotes/
http://help.github.com/git-cheat-sheets/
http://gitready.com/beginner/2009/01/21/pushing-and-pulling.html

