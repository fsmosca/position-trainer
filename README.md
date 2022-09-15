# Position-Trainer
Simulate from positions with bad moves.

## Setup

* [Download](https://www.python.org/downloads/) and Install python version >= 3.7
* Clone this repository see sample below.

```
PS F:\Tmp> python --version
Python 3.10.6
PS F:\Tmp> git clone https://github.com/fsmosca/position-trainer.git
Cloning into 'position-trainer'...
remote: Enumerating objects: 42, done.
remote: Counting objects: 100% (42/42), done.
remote: Compressing objects: 100% (28/28), done.
remote: Total 42 (delta 12), reused 34 (delta 10), pack-reused 0
Unpacking objects: 100% (42/42), done.
PS F:\Tmp> cd position-trainer
PS F:\Tmp\position-trainer> ls


    Directory: F:\Tmp\position-trainer


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        2022-09-16     00:03                engine
d-----        2022-09-16     00:03                library
d-----        2022-09-16     00:03                pgn
-a----        2022-09-16     00:03           1928 .gitignore
-a----        2022-09-16     00:03           6130 app.py
-a----        2022-09-16     00:03          35823 LICENSE
-a----        2022-09-16     00:03             61 README.md
-a----        2022-09-16     00:03             18 requirements.txt


PS F:\Tmp\position-trainer> pip install -r requirements.txt
PS F:\Tmp\position-trainer> streamlit run app.py
```

The command `streamlit run app.py` will run streamlit server and a browser will be opened.

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.254.104:8501
```

### Load and analyze games

![image](https://user-images.githubusercontent.com/22366935/190454799-c6e09b56-5597-488f-b5bb-d099a494a4a6.png)

### Train

![image](https://user-images.githubusercontent.com/22366935/190455075-e6f039d8-a65d-437e-94c3-81ea7a093399.png)

### Engine

The engine that is used to analyze the moves is in the `engine folder`. It is a stockfish 15 for modern hardware. You may replace it
but be sure to keep the filename sf15.exe.


