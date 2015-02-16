# Thoughts behind project's architecture decisions


## Accounts

**Why `Account` and not `AbstractBaseUser`?**

`AbstractBaseUser` has everything the project needs except `gender` field.
It's more DRY and easier to maintain if I extend the super class.

## Activities

**Why `Activity` of all types and not concrete classes ex. `ProfilePost`, `PublicationLike`?**

All of posts, likes, comments and etc are __activities__. It makes more sense to me to have one class for that.
IMO aggregation and signals registering is more sane, but maintainability may suffer a bit.


## Feeds

Are like `Linkedin's pulse`. They contain only `Publications`. Of course you can comment/like them using `Activity`.


## Profiles

Are essentially a wrapper for our extended `AbstractBaseUser` - `Account`.

**Why create a new class for that?**

`Profiles` may have many more fields like `interests`, `groups`, `photos` and etc.
Having a separate class for that gives me more possibilities to add features.


**You just want to fake-delete profiles as Facebook does?**

![Uncovered truth](http://www.court-records.net/animation/atmey-damage.gif "Uncovered truth")

