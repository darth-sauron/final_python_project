# final_python_project
s26250

This is a very simple application, which allows the user to create a simple DnD character following the 5e rules. First all the information regarding races and classes is scraped from a dedicated website (which was kind enough to allow to make a request using code, unlike some other websites) and this information is stored 
in json files (two separate ones for classes and races). Then the data from those files is processed into the database for a more convinient use later on.

Now for the GUI part. The whole application actually starts with a login/registration window where the user either logs in (i know, shocker) or registers. For various errors there are message boxes in place which will let the user know that something isn't right.
Once the user logs in they can make their character (whoopi). Theres is a menu bar at the top, where they can selsect what they want to do. They can choose a race,
which is a list of all the available ones (we wouldn't want the users to just invent their own, would we). Associated with each one is a list of stats, so that the
user would know which die to use for hp, and which abilities are modified by that race. Once they settle on the one they like they can choose it and it will 
automatically transport itself into the "race" field of the forming character. Exactly the same process is applied to "choose classes" menu. There are also 4 labels
(aka dice) on the bootom of the screen. They are, in fact, there to simulate rolling of dice. As we all know we need four to the then chuck out the least of them
and to sum up the remaining three and then put that number in one of the ability scores. The "dice" are "rolled" by simply clicking on them. As simple as that.
For thing that require something other than d6 there is a menu for dice, which will open another window allowing the user to choose any die from d2 to d20 and any
number of them ranging from 1 to 10. It is possible to roll them all simultanipusly by pressing a button or each one individually by clicking them. Once that is
done the user can click the very-cleverly-named button "Done" or just exit the window. The remeining work is just to input the correct values into their respective
fields (not just any value will be accepted mind you) and creating a name for the character. And voila, once the "Create Character" button is clicked the character 
is, indeed, created. What joy. 

Now, of course, what is the point of creating a character if you cannot access them later? To that end there is one last feature. In the character menu there
is an option to view characters, where there is a new window with all the characters belonging to that user. The user can then modify most of the fields (becuase 
we all know things happen during the game). 

That's pretty much it. Sweet and to the point, i would say. 
