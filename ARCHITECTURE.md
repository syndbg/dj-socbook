# Thoughts behind project's architecture decisions


## **Accounts and Profiles** [already refactored]

**Why `Account` and not `AbstractUser`?**

`AbstractUser` has mandatory fields that will be utilized in the project.
I want to add a bit more so I would just extend it. Re-inventing `AbstractUser` from scratch is a bad practice in this case.

**Profiles?**

Are just a wrapper for accounts providing an `url` and publicity as accounts are never private, but their info can be.

**You created the wrapper to just fake-delete profiles as Facebook does?**

![Uncovered truth](http://www.court-records.net/animation/atmey-damage.gif "Uncovered truth")



## **Activities and Notifications** [already refactored]

Activities are everything that shows up on an account profile or the global (public) activities page.
Notifications are more personal. They are updates about things regarding you in the social network. Making friends, interacting with people and plethora more.



## **Feeds** [to be refactored]

~~Are like `Linkedin's pulse`. They contain only `Publications`. Of course you can comment/like them using `Activity`.~~
I'm wrong. `Feeds` or `Publications` are `likes, comments` and etc. What I was trying to do is also an option, but
it's not the most optimal approach. It would've left `Activities` with too much responsibilities.
