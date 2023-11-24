## Local build

First clone this repo using the command `git clone`. 

Once you have the project files locally you can follow the instruction below to build the html book example using quarto environment.


## Running the example on visual studio code

An easy way to manage your project and git is through visual studio code. You need to do the following step-by-step:

1. Open VS code, select "File" and open the folder you just cloned from the repository.
2. Check the extensions installed. The following extensions are required for the project. You can install those extensions by clicking the tool box icon on the side bar and searching for each one by its name, then clicking "Install".
    * Python, by Microsoft
    * Quarto, by Quarto
    * R, by REditorSupport
    * Git History, by Don Jayamanne
    * Git Graph, by mhutchie
3. Open the terminal bar in VS code.
4. Input `quarto check` in the terminal and then `enter` to check the environment setting of you quarto. 
5. Input `quarto preview` in the terminal to open a temperary report on your browser. It may take 1~2 minutes for your first run. You can edit the content in the `qmd` file and the report will adapt the changes automatically when you save them. 
6. you can also use the `render` function by opening a new terminal and inputting `quarto render` in the terminal to generate a report in html format in the `_book` folder.

More information about quarto can be found [here](https://quarto.org/docs/get-started/)