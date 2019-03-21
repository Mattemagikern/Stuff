set this in your bashrc:
export PYTHONDONTWRITEBYTECODE=1.
it will tell python not to create __pycache__ directories every where. which is
nice to be without.
you lose a bit in efficiency but gain a lot in not having to see the directorie
in the root folder of your project.


can recomend reading:
https://www.amazon.com/Python-Testing-pytest-Effective-Scalable/dp/1680502409

It will give you a deeper understanding of pytest and how it operates.

Important note: fixtures stack in order of execution. Ex session is executed
before modules and functions etc.


Best of luck! 

//Måns Ansgariusson

