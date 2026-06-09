Welcome back to GitHub for Beginners. This is the final episode of the season, and we’ve covered a lot so far. Make sure to check out our other episodes to see all the various topics we’ve discussed.

Today, we’re going to spend some time answering some questions that people often have, especially when they’re first getting started. So without further ado, let’s jump right in.

What is SSH and how do I add my SSH key to GitHub?

An SSH key is a secure shell key. It’s a pair of files on your computer that has two parts: a private key and a public key.

The private key stays on your computer and should never be shared. The public key is what you share with platforms like GitHub. When you store your public key on GitHub, git uses your private key to confirm your identity when you push and pull code. In order for you to be authenticated, your public key on GitHub needs to match the private key on your computer.

So how do you do this? Let’s create a key pair and add your public key to GitHub now.

(And remember, if you prefer a video walkthrough, that is available.)

Open up a terminal and enter the following command. Remember to replace the email placeholder with your email address you use to log into GitHub.

ssh-keygen –t ed25519 – C YOUREMAIL@DOMAIN.COM

When it prompts you to enter a file to save the key, press Enter to accept the default file and location.

Enter a passphrase that you’ll remember. Note that the terminal will not display what you type, so be careful not to have any typos!

Reenter your passphrase.

This will create your new SSH key. Now you want to add it to your ssh-agent. An ssh-agent is a program that securely stores your keys so that you don’t need to keep entering your passphrase.

Click your profile picture in the top-right corner and select Settings.

In the menu on the left-hand side, select SSH and GPG keys.

On the right-hand side, click the green New SSH key button.

Give the key that you’re about to add a name in the “Title” box that describes this key in a way you’ll remember. For example, if this is your work laptop you might enter a title of “work-laptop”.

Paste the key you copied from the terminal into the “Key” box.

Click the green Add SSH key button at the bottom of the window.

Congratulations! Your computer is now configured to connect to GitHub over SSH.

How do I add a PAT to GitHub? What is a PAT?

PAT stands for Personal Access Token. A PAT is a special credential that you create on GitHub for tools that need authentication. You control its permissions and can revoke it any time. On GitHub, you’ll commonly use a PAT to authenticate via command line or the GitHub API.

There are two types of PATs available: fine-grained tokens and classic tokens. First we’ll walk through creating a fine-grained PAT.

Click your profile picture in the top-right corner and select Settings.

Scroll to the bottom of the list of options in the left-hand column and select Developer settings.

In the left-hand column, expand the option for Personal access tokens. Select Fine-grained tokens from the options displayed.

Click the green Generate new token button in the center of the window.

Enter a name and description for the token. This should make it clear what the token is going to be used for (e.g., a name of “cli-access” with a description of “access the Copilot CLI”).

Under “Expiration,” select a date that matches how long you need the token to be valid. Once the token expires, it will not work anymore.

Under “Repository access,” select which repositories you want the PAT to be able to access. You can limit the selection to only specific repositories if you know which repositories it will need to access.

Under “Permissions”, click Add permissions to select which permissions you’re granting to this PAT. This lets you define the scope of what the PAT can do.

For each permission, you can specify whether it has read-only access or read and write access.

When you’re satisfied with the permissions, scroll to the bottom and click the green Generate token button.

A window pops up, providing a review of all of the information associated with this token. Verify that the information is correct, and then click Generate token.

GitHub will now show you the token. Make sure that you copy it and store it in a safe location (e.g., a password manager), because GitHub only shows you this token once.

Click your profile picture in the top-right corner and select Settings.

Scroll to the bottom of the list of options in the left-hand column and select Developer settings.

In the left-hand column, expand the option for Personal access tokens. Select Tokens (classic) from the options displayed.

In the main window, click Generate new token and select Generate new token (classic).

Give the token a clear name that explains what it will be used for (e.g., “terminal-access”).

Under “Expiration,” select a date that matches how long you need the token to be valid. Once the token expires, it will not work anymore.

Select the scopes for your token. The scopes indicate what access permissions the token grants.

When you’re satisfied with the scopes, scroll to the bottom and click the green Generate token button.

GitHub will now show you the token. Make sure that you copy it and store it in a safe location (e.g., a password manager), because GitHub only shows you this token once.

This creates the classic token. The next time that GitHub asks for your password in a terminal, instead of supplying your password, you could paste this token.

What’s the difference between merging and rebasing, and how do I fix a merge conflict?

A merge conflict is what happens when two changes touch the same part of a file, and git needs your help to decide what the final version should be. There are a few different ways you can resolve this, but we’re just going to walk through it using the GitHub UI.

Open a pull request that has a merge conflict. GitHub will provide a message indicating that there’s a conflict and you won’t be able to automatically merge.

Scroll to the bottom and click the Resolve conflicts button inside the warning about conflicts.

GitHub opens the files that have conflicts. Use the editor to resolve the conflicts by choosing which version of the file to use in each case where there’s a conflict.

Once the file has no more conflict markers (i.e., you’ve addressed every conflict), select Mark as resolved in the top-right.

Repeat this process for every file that has merge conflicts.

After you’ve addressed all the files that have conflicts, click the green Commit merge button at the top of the window.

This updates your pull request with the merged conflict and now you’ll be able to merge that change into your repository. Well done!

Now let’s talk about the difference between merging and rebasing, and when you might want to use one over another.

Merging combines changes from one branch into another by creating a new commit that ties both histories together. It preserves the history of both branches. You should merge when you want to preserve the full history of how work happened. This is commonly used for feature branches that are going to be merged into main, such as when you’re adding new functionality.

On the other hand, rebasing moves or replaces your branch’s commits on top of another branch. It rewrites the history to create a linear and cleaner commit timeline. You should rebase when you want a clean linear history, like when you are updating your feature branch to pull in the latest changes from main. For example, if you are working on a feature, but you want to pull in the latest changes from main before merging.

How do I undo my last commit?

Let’s say that you’re in a situation where you’ve already pushed your commit to your branch, and you want to undo it. You can undo your commit through the GitHub UI.

Open the commit that you want to undo on github.com.

Scroll to the bottom of the commit and select the Revert button.

GitHub creates a new commit that undoes the changes from your previous commit. It’s important to realize that this doesn’t erase the commit history, but rather puts a new change in place that undoes your previous changes. You can now either merge this commit directly or open a pull request with it. Opening a pull request is the safest option when others might be using the branch.

If your changes are local, and you haven’t yet pushed to a branch, you can locally revert your commit by running the following command.

git reset --soft HEAD~1

This removes the commit from your local repository, but keeps your work staged so that you don’t lose any changes. If you would rather undo your changes even locally to reset your workspace, you can use the following command. Just realize that by doing this, you might lose your work!

git reset --hard HEAD~1

How do I update or sync a forked repository on GitHub?

Forking a repository creates your own copy of a project so that you can explore or make changes to it without affecting the original repository. This is especially important when you want to contribute to an open source project. Here’s how you can fork a repository.

Open the repository that you want to fork on github.com.

Select the Fork button at the top of the repository.

Choose the Owner of this forked version, which in most cases will be your GitHub account.

You may optionally rename the repository by providing a new Repository name. By default, forked repositories keep the names of the upstream repository.

At the bottom of the window, select Create fork.

This creates a full copy of the project under your account. To work on it locally, select the Code button and clone it to your machine.

Now that you’ve created the fork, you want to make sure that you still pull in the latest changes from the upstream repository. Otherwise, your forked copy can quickly become out of date.

Navigate to the main page for your forked repository on github.com.

At the top of the repository, select the Sync fork button.

Select Updatebranch in the pop-up menu.

When you do this, GitHub automatically pulls in the latest changes from the upstream repository to keep your fork up to date. You can also do this from the command line.

Open a terminal and navigate to your repository.

Set the upstream repository. Make sure to update the URL in the following command with your original repository URL.

Merge the latest changes into your project. Note that the following command assumes that the upstream project uses main as the default branch. If it uses something else, you will need to use that branch in the following command.

git merge upstream/main

This updates your local copy with all of the changes to the upstream branch. So now, you need to push them to GitHub to make sure your repository is synchronized.

git push origin main

Now you know how to work in your own copy of a project and keep your work synchronized!

How do I review a pull request on GitHub?

A pull request (often abbreviated PR) is a place to share code and talk about changes. Here are three helpful practices to keep in mind when you’re reviewing a pull request.

Start by understanding the goal of the pull request. Open the pull request and read the description. See if it has an associated issue, any screenshots, or notes from the author. Knowing the purpose helps you know why the changes exist and what you’re looking for.

Review the code changes in small sections. Open the Files changed tab and move through the changes one group at a time. If something isn’t clear, leave a comment on that line. Ask questions, offer suggestions, or let the author know if you see a better approach. Keep your comments specific so they know exactly what you’re referencing. It might help to open the code on your machine either via the command line or in a codespace to run the code yourself to ensure you understand. Use terms like “nit” if your comment is not a necessary suggestion for merging the pull request.

Highlight what’s going well. When you see code that’s well organized, thoughtful, or teaches you something, mention it! Positive feedback reinforces good patterns and helps teammates feel supported.

When everything looks ready, use the Submit review button to approve the changes or request updates.

Copilot code review can also help you understand pull requests and suggest improvements. Note that in order to use Copilot, your organization admin needs to enable Copilot for either your repository or your user account. Once Copilot is enabled, you don’t need to install anything special—Copilot code review will automatically appear as an option in pull requests.

Open a pull request on github.com where you want to use Copilot code review.

Select Reviewers in the top-right.

Select Copilot from the list of suggested reviewers.

In a short amount of time, Copilot will complete its review. You can scroll down and see the comments left by Copilot. It always leaves a “Comment” type of review, not an “Approve” or “Request changes” type of review. This means that Copilot reviews do not count toward required approvals nor will they block merging changes.

And that’s a wrap! With this episode, we’ve finished another season of GitHub for Beginners, ending with some of the most common questions we’ve seen or heard. We hope that you found this information helpful, and don’t forget to check out our full library of GitHub for Beginners topics.

Kedasha is a Developer Advocate at GitHub where she enjoys sharing the lessons she's learned with the wider developer community. She finds joy in helping others learn about the tech industry and loves sharing her experience as a software developer. Find her online @itsthatladydev.