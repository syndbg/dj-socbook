# Thoughts behind project's architecture decisions


## **Accounts**

**Why `Account` and not `AbstractUser`?**

`AbstractUser` has mandatory fields that will be utilized in the project.
I want to add a bit more so I would just extend it. Re-inventing `AbstractUser` from scratch is a bad practice in this case.


## **Activities**

~~**Why `Activity` of all types and not concrete classes ex. `ProfilePost`, `PublicationLike`?**~~

~~All of posts, likes, comments and etc are __activities__. It makes more sense to me to have one class for that.
IMO aggregation and signals registering is more sane, but maintainability may suffer a bit.~~

I mix up `Publications` with `Activities`. To-be refactored.


## **Feeds**

~~Are like `Linkedin's pulse`. They contain only `Publications`. Of course you can comment/like them using `Activity`.~~
I'm wrong. `Feeds` or `Publications` are `likes, comments` and etc. What I was trying to do is also an option, but
it's not the most optimal approach. It would've left `Activities` with too much responsibilities.


## **Profiles** - now part of **Accounts**

Are essentially a wrapper for our extended `AbstractBaseUser` - `Account`. (They are after the updated answer)

**Why create a new class for that?**

~~`Profiles` may have many more fields like `interests`, `groups`, `photos` and etc.
Having a separate class for that gives me more possibilities to add features.~~

^ This is kind of wrong too. Most user info data should go to `Account` and leave `Profile` with `OneOnOne Account` and `CharField url`.
This is much cleaner.


**You just want to fake-delete profiles as Facebook does?**

![Uncovered truth](http://www.court-records.net/animation/atmey-damage.gif "Uncovered truth")

