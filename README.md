This README focus on how to set up you computer to scrape informations from the website: https://books.toscrape.com/
Using this program will allow you to save books informations on csv files which can be opened with Excel or OpenOffice
You also have pictures from each books saved at jpg format in a separate repository 'Pictures'

Be careful: - For each code line found in the README between "", take only the text and forget about ""
	    - To paste code line in you powershell windows (cf after in this README) use the right clic + paste (don't use ctrl + v)

PYTHON INSTALLATION:
To run this code you need Python 3.8 version or further 
Download python's executable file on the following website: "https://www.python.org/downloads/"
Lauch the installation without any modification.

CREATION OF THE WORKING REPOSITORY:
To run this code and find the informations you seek for, you need to create a working folder.
With the Windows explorer go at the place you choose to work, create a new working folder. 

SET WINDOWS TO THE RIGHT PLACE (your woking folder pathway):
You now need to open windows powershell to install necessary modules and use the code: 
on you keyboard, use windows + x and choose Powershell(admin) and answer yes 

In the new blue windows, you have to put your working folder's path
For that go back to your windows explorer, go in your working folder
now you're in , copy the pathway of your folder found in the adress bar (C:\Users\...\....)

In the PowerShell(blue window) type: cd "yourfolderpathwaythatyoujustcopied" (this time keep the quote marksand let a space after cd) and ENTER
D
Your computer knows right now where it have to work

CREATE A SPECIAL WORKING ENVIRONMENT:
With Python, you have to create a special working environment to install specifics modules for each project.
In the PowerShell using the following command will set a new environment 'env':
"python -m venv env" and ENTER

You now need to activate it, for that use:
"source env/Scripts/activate" or source env/Scripts/activate.bat and ENTER

if you have any issue to activate your environment:
-go to the env folder and search for the folder name which contain the "activate" file 
-replace "Scripts" by this name

With that you working environment is active 

DOWNLOAD REQUESTED FILES AND MODULES:
go to the following repository: https://github.com/Satupathe/requests
-find the green button clic on the arrow 
-clic on the arrow
-choose download ZIP
-download the zip file
-extract its content and put requirement.txt, the scraping folder, README.md and the main.py in your working folder

now use this command on the Powershell:
"pip install -r requirements.txt"

This step install necessary modules to execute the code

LAUNCH OF THE CODE AND SAVED BOOKS INFORMATIONS:
In the PowerShell type "python main.py" and ENTER
it will launch your scraping program and you'll soon see a new folder 'category files' containing all the needed informations

This code make it through the website within near 15 minutes. let it work and when it finished you'll see appear messages on you PowerShell.
You should see 'Scraping finished'

you now can quit the PowerShell using the closing button

Thank for reading this README and using my program