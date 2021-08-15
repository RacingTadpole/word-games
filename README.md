# Word game solvers

## Boggle

Discover all the words in your Boggle board!

For example:

```
Enter a board with commas between rows: racin,gtadp,olera,cingt,adpol

                RACIN
                GTADP
                OLERA
                CINGT
                ADPOL

4 letters: 107  |  5 letters: 78  |  6 letters: 44  |  7 letters: 12

      rate     rated     rater    racial     argot     acted      acid     cargo      cart    cartel    carted    carter
     cater    calico      cain      cade     cadet      care     cared      card      carp     carat    carton     cider
    cinder      idea     ideal     grate    grated    grater     going    garter      gate     gated      glia      glad
     glade     glare    glared      glen      toga      toil    toiled    toiler      taal      talc      tale      tarn
      tart      teal      tear      tend      tern      alga      alto     altar     alter     alien     aline    alined
     alert      aide     aider      aden     adage     argon      data      date      dale      dare      darn      dart
    detain   deltoid     delta      deli      deal     dealt   dealing      dear      dial    dialog   dialing      drat
     drain      drag   dragnet    dragon      pica      prat   praline   predict     padre    parade      pare     pared
      part      page     paged     pager    ogling      ogle     ogled     oiled     oiler      loci      loin      lien
      lied      line    linear     lined     liner    linger      lino      late     later      laid      lain      lade
     laden      lard     large     largo      leat      lead     learn      lend    legato      etal      earn     edict
      ergo     ergot      raid      rain    retain     relic    relaid      rein      real     react      read    redial
   radical   radiate    radial      rage     raged     rapid      area     areal    agenda      aged    atonic     atone
    atoned      atop      colt      cola      cole      coil    coiled      coin    coined    coiner      clog      clot
     cling      clip      clad    claret     cleat     clear      cleg      cine      iota    inlaid     inlet     inert
   ingrate     ingot      nile      neat      near      nerd      gear     grain     grade     great      gone    garnet
    garden     tract     train      trad     trade   tradein     treat     tread     trend      trap     tonic      tone
     toned     toner     tonga     topic    target    dilate   dilated      diet      died      dine     dined     diner
      ding    dinged     dingo     pilot   piloted      pile     piled     pieta      pied      pier      pine    pineal
     pined      ping      pond      oner     opine    opined      ogre      lone     loner      long    longed    longer
    loping

Total: 241 words
```

## Word Ladder

Solve the word ladder game, where you provide two words
of the same length, and need to change one word into the other, changing
only one letter at a time, while only forming valid words.

```
Enter the starting word: party
Enter the target word (if any): grows

2 optimal solution(s) of length 9 found:
party → parts → carts → carps → corps → coops → crops → crows → grows
party → parts → ports → sorts → soots → slots → slows → glows → grows
```

Or find the hardest words you can from a given starting word, eg.
```
Enter the starting word: party
Enter the target word (if any):

Final words: above, aloud, anode

1 optimal solution(s) of length 18 found:
party → pasty → paste → passe → posse → poise → prise → prose → prone → crone → clone → alone → aline → amine → amide → abide → abode → above
```

## Make five

This is still a work in progress, but you can do the following:

```
python -m make5.solve

Enter your grid with commas between rows, and . for empty (eg. .....,...n.,f..a.,t..nk,....s)
? .....,...n.,f..a.,t..nk,....s

                  01234
                0 ?????
                1 ???N?
                2 F??A?
                3 T??NK
                4 ????S

Enter the new letter: O

Best locations (analysing depth 1):
(1, 2):  72.1  upony  ufond  whonk  upond  muons  phony  /  comfy  bobby  poppy  youch  cocky  popup
(1, 4):  53.8  hymn.  upon.  spun.  shun.  cyan.  faun.  /  bob..  bop..  bow..  box..  boy..  cob..
(2, 1):  53.4  ..bap  ..bay  ..cab  ..cam  ..cap  ..caw  /  ufoxy  ufolk  ufoul  whock  chomp  smoky
(4, 1):  50.6  bomb.  cock.  comb.  coup.  jock.  mock.  /  jumbo  bimbo  pluto  duomo  hippo  limbo
(3, 1):  49.6  top..  tow..  toy..  .own.  tog..  ton..  /  buxom  bijou  yukon  phlox  bosom  fluor
```

This shows the top few locations to place the letter, based on the expected scores of the rows and
columns (weighted by the likelihood of getting the required letters).
It does not yet consider the consequences of placing the letter on other rows and columns.

You can also use:

```
python -m make5.play_line
```

to get all the words matching a pattern, ranked by their scores weighted by the likelihood of getting the remaining letters.
The score shown for each is calculated using a score of 1 per letter per subword.

## Quick start

### Install Python and pipenv

See the [pipenv documentation](https://docs.pipenv.org/install/) for the steps to install python 3, pip and pipenv.

On a Mac, you will need to install python 3 as described above (python 2 is the default).
The simplest way to install `pipenv` is to install homebrew, and then type `brew install pipenv`.
 
On linux, this [link](https://packaging.python.org/install_requirements_linux/#installing-pip-setuptools-wheel-with-linux-package-managers)
may be helpful.

### Install the Required Packages

Enter the `boggle` directory, and type:

```
pipenv install --dev
```

This creates an environment containing the required packages, which you enter by typing:

```
pipenv shell
```

### Download a word dictionary

Eg. http://www.mieliestronk.com/wordlist.html . Use lower-case.

Save as `words.txt` in the `data` directory.

### Run

Just type one of:

```
python -m boggle.solve
```

or

```
python -m word_ladder.solve
```

### Run the tests

In the pipenv environment, make sure this command runs without error:

```
bin/check_code
```

### Install PyCharm or equivalent

Install PyCharm or a similar editor. A vanilla text editor is fine too.

### Use this repo as a template for your own python project

You can clone this repo, and type

```
bin/rename foo_bar
```

to get it ready to use as a project named "foo_bar".

Note to finish the process properly, you should then do the following:
    1. `rm -rf .git`
    2. Update `README.md`
    3. Update the description and author in `setup.py`
    4. `git init && git add --all && git commit -m 'initial commit'`
