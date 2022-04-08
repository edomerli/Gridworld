# Grid World

Setting Up
----
First, make sure you have Python 3.\* and the latest pip >= 20.\* (Check the `Notes & FAQ` section below if you're having trouble with this). Then, here is the preferred way to set up (if you have another way, feel free to do it):

1. Install [anaconda](https://docs.anaconda.com/anaconda/install/) to set up a virtual environment
2. `conda create -n cse150b python=3.10`
3. `conda activate cse150b`
4. To install PyGame, `pip install pygame`. We will use PyGame for all assignments in this class.
 
You can run `conda deactivate` to deactivate the environment. The next time you want to work on the assignment, type `conda activate cse150b` first to use the exact same environment with PyGame installed.

Game
----
The gameboard is a grid and each cell has a different weight assigned to it depending on the type:

- road (grey cell): +1
- grass (green cell): +10
- puddle (blue cell): +infinity (i.e. can't be walked on)

Initially all tiles are unexplored. Then they get colored differently when they belong to these different sets:

- explored &#8594; lighter color
- frontier &#8594; white

Problem statement
----
The task is to find paths from the start (yellow node) to the goal (orange node). Once you load up the program (You'll see how in the `Usage` section below) and press `enter` you will see what that means. The algorithms implemented are:

- DFS
- BFS
- Uniform Cost Search (UCS)
- A\* Search using Manhattan Distance as the heuristic

UCS and A\* take the weights into account, and find the minimum cost path. DFS and BFS don't (obviously since it's not within their capabilities)

Usage
----
Simply run `python main.py` and you will see the grid world window. By pressing `enter` you see how DFS finds a path. Pressing 2, 3, or 4 should respectively run BFS, UCS, A\* in a similar way. Other commands are visible in the legend at the top once the game is loaded.

The `tests` file contains a few test maps. If you want to load in the maps as test cases (`python main.py -l [test case number]`), we have provided a few fun cases for you to play with:

0. Random 1
1. Random 2
2. Spiral
3. Zigzag
4. "Two roads diverged in a wood, and I - I took the one less traveled by, and that has made all the difference."
5. CSE ~~11~~ 150b style (homage to Rick Ord)
6. "It's a-me, Mario!"

You can also do `python main.py -t` which autogrades the algorithms with respect to the correct optimal costs in the seven maps above.

Tips & FAQ
------
**Why does `python` show up as Python 2.\* instead of Python 3.\*?**
- If `python --version` shows Python 2.\*, but `python3 --version` shows Python 3.\*, you will either need to run all your commands with `python3` (e.g. `python3 main.py`) or change your default `python` to Python 3.\*. Here's a [link](https://askubuntu.com/questions/320996/how-to-make-python-program-command-execute-python-3) that shows you how to set `python` to Python 3.\* by default instead of Python 2.\*. 

**My pip shows a version lower than 20.\*; how do I update it?**
- First, check if you have the right Python version; your pip version should be up to date if you have the correct Python. If this isn't the case, check [this](https://pip.pypa.io/en/stable/installation/#upgrading-pip) out.

**My system says `pip not found` when I try to run `pip`. What do I do?**
- First, check that you have Python 3.\* installed correctly. If you can't find any problems there, here's a [resource](https://pip.pypa.io/en/stable/installing/) you can check out.
