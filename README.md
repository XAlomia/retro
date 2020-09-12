# retro
analysis, research and visualizations from retrosheet data 

The retrosheet data is too large to add to github repo, I have it named in these files retro_events.csv 
However, please make sure the files retro_events.csv are in your local drive. 

How to process the retrosheet data (I am using Windows for these instructions): 
1. Go to https://www.retrosheet.org/game.html and use any 'regular season event file' you want to use. 
  I downloaded decades 2010-2019 and 2000-2009, download them to your local disk
2. Download the Chadwick executables at https://github.com/chadwickbureau/chadwick/releases, using version 8.1. Unzip 
   the file and move all the .exe files to your local disk
3. For each year of the 'regular season event files' you want to use run the command below 
  cwevent -y 2018 -f 0-96 2018*.EV* >> retro_events.csv in the terminal 
  // so if you want just 2017, change 2018 to 2017 and etc 
4. Move the file to /retro 

Updated 9/12/2020
