## 猫 (neko)
Neko is an experiment to build a single player game foundation on the LambdaMOO world idiom. LambdaMOO is a multi-user programmable object environment. It feels a bit like Smalltalk but it's more specialized and multiple users can edit and use objects at the same time at runtime, it also has a task scheduler and no graphics. Not suprisingly, it also originated at Palo Alto during the end of the first golden age of software.

The LambdaMOO design is quite elegant and the code is fantastic to behold. It has a lot of stuff going on and should be recommended reading for every programmer.

## Commands
Neko operates on text commands with the following syntax:

    <verb> [<direct object>] [<preposition> <indirect object>]

Command parsing is broken up into a few discrete stages which are explained below.

#### Tokenizing
First, the command is tokenized so that (for example) `'foo "bar mumble" baz" "fro"tz" bl"o"rt'` is tokenized into `['foo', 'bar mumble', 'baz frotz', 'blort']`. This job is performed by the `tokenizer.tokenize` function. 

#### Parsing
From this set of tokens, the `command.parse` function assumes the first one to be the verb. Then it looks if it can find a preposition (e.g. `in`, `from`, `on`). If it does then all the tokens before it are considered to be the direct object and all the tokens after it will be considered the indirect object. If we don't find a preposition then everything (except the verb) is considered to be the direct object. In any case, all object tokens are joined back together into a single string (using a space character).

#### Resolving
After this we have a raw command specification but we can't really do anything with it yet before we resolve it in the game world. We can do this by feeding the parse output into the `world.resolve` function. This will return an even better command dictionary where hopefully all the object references such as `iobj` and `dobj` have been filled in.

Also, if a valid command was supplied, this updated command dictionary should point to a function on an object somewhere in the game world. The game runtime is responsible for executing this function using the rest of of the information available from the command dictionary.