# Lotto SA Stats

This is a evolving project I use to learn about stats.

I base my learning on data from the South African lottery.

This is for personal development and not meant to be used in any real world project. Thing may (and probably will) break.

At the time of writing this README, I am still busy putting together the Domain Model.

## Notes

How the all_boards.py file was created:

    cat balls_played.txt | python ball_splitter.py > all_boards.py

The file `balls_played.txt` contains the data with the following syntax:

For Powerball game:

    Board <NAME> <NUM> <NUM> <NUM> <NUM> <NUM> Powerball: <NUM>

For Lotto game:

    Board <NAME> <NUM> <NUM> <NUM> <NUM> <NUM> <NUM>

Example:

    Board A 11 25 27 42 43 Powerball: 2  

    Board A 4 16 23 37 42 49


Only two games are supported at the moment: The Lotto and PowerBall games.

Note: The numbers I used was selected randomly, but I use them consistently throughout the project at this stage. Perhaps later I will create a random selector as well.
