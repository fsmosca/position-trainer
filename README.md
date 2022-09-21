# Position-Trainer
Test your skill to find the best move from the given test position where the player from the test sets fails to find. It generates a summary table with your selected move, the game move and the engine move. The test sets in json format can be found under the data folder.

You can also generate test positions with the use of `test_generator.py` which can be found in this repository. You need the [stockfish](https://stockfishchess.org/) engine to analyze the positions where the test_generator saves interesting positions in json format. There is also a stockfish 15 compiled for modern hardware under the engine folder.

Take a pgn file from [the week in chess](https://theweekinchess.com/) for example and generate test positions. It is better if the players have WhiteElo and BlackElo in the PGN because Position-Trainer can filter rating range and you can train on positions from those players with that filtered rating.

## Setup

### 1. Open the app from the cloud.

Go to this address https://fsmosca-position-trainer-app-nfsbbl.streamlitapp.com/

Download the json training file inside the data folder or from [here](https://drive.google.com/drive/folders/1Epmc0EXAldKRJ41IaW9dOWEg3OO-uvgc). It is a test file that is needed for training.

### 2. Run the app locally from your browser

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

### Train

![image](https://user-images.githubusercontent.com/22366935/191387009-2ebf4e2a-9c87-460c-b9bf-e714d35dac9d.png)

## Generate training file in json format

Use the **test_generator.py** program to generate test positions.

You need to install python chess with:  

`pip install chess`

**Command line**  
```
python test_generator.py --pgn-file ./pgn/stlbli22_4games.pgn --engine-file ./engine/sf15.exe --engine-hash-mb 128 --output-file mytest.json --movetime 1000
```

### Sample output

```
{
    "5rk1/6pp/1q6/p2p1pQ1/1n3N2/6P1/2r2P1P/R4RK1 w - -": {
        "stm": "white",
        "fmvn": 34,
        "hmvc": 6,
        "game": {
            "move": "Nh5",
            "score": -237,
            "rate": 0.29
        },
        "engine": {
            "move": "Qe7",
            "score": 0,
            "rate": 0.5
        },
        "user": {
            "Qd8": {
                "score": -1229,
                "rate": 0.01
            },
            "Qxg7+": {
                "score": -1090,
                "rate": 0.02
            },
            "Qe7": {
                "score": -20,
                "rate": 0.48
            },
            "Qh6": {
                "score": -1159,
                "rate": 0.01
            },
            "Qg6": {
                "score": -1210,
                "rate": 0.01
            },
            "Qf6": {
                "score": -1194,
                "rate": 0.01
            },
            "Qh5": {
                "score": -91,
                "rate": 0.41
            },
            "Qxf5": {
                "score": -1132,
                "rate": 0.01
            },
            "Qh4": {
                "score": -84,
                "rate": 0.42
            },
            "Qg4": {
                "score": -1272,
                "rate": 0.01
            },
            "Ng6": {
                "score": -832,
                "rate": 0.04
            },
            "Ne6": {
                "score": -799,
                "rate": 0.04
            },
            "Nh5": {
                "score": -232,
                "rate": 0.29
            },
            "Nxd5": {
                "score": -794,
                "rate": 0.05
            },
            "Nh3": {
                "score": -262,
                "rate": 0.27
            },
            "Nd3": {
                "score": -850,
                "rate": 0.04
            },
            "Ng2": {
                "score": -297,
                "rate": 0.24
            },
            "Ne2": {
                "score": -900,
                "rate": 0.03
            },
            "Kg2": {
                "score": -144,
                "rate": 0.37
            },
            "Kh1": {
                "score": -272,
                "rate": 0.26
            },
            "Rfe1": {
                "score": -31998,
                "rate": 0.0
            },
            "Rfd1": {
                "score": -31998,
                "rate": 0.0
            },
            "Rfc1": {
                "score": -31998,
                "rate": 0.0
            },
            "Rfb1": {
                "score": -31998,
                "rate": 0.0
            },
            "Rxa5": {
                "score": -682,
                "rate": 0.07
            },
            "Ra4": {
                "score": -132,
                "rate": 0.38
            },
            "Ra3": {
                "score": -111,
                "rate": 0.4
            },
            "Ra2": {
                "score": -888,
                "rate": 0.03
            },
            "Rae1": {
                "score": -121,
                "rate": 0.39
            },
            "Rad1": {
                "score": -79,
                "rate": 0.42
            },
            "Rac1": {
                "score": -141,
                "rate": 0.37
            },
            "Rab1": {
                "score": -209,
                "rate": 0.31
            },
            "g4": {
                "score": -499,
                "rate": 0.13
            },
            "h3": {
                "score": -84,
                "rate": 0.42
            },
            "h4": {
                "score": -79,
                "rate": 0.42
            }
        },
        "analysis_engine": "Stockfish 15",
        "analysis_movetime": 1.0,
        "analysis_depth": 1000,
        "header": {
            "Event": "44th Olympiad 2022",
            "Date": "2022.07.29",
            "Round": "1.1",
            "White": "Masango, Spencer",
            "Black": "Erigaisi, Arjun",
            "WhiteElo": "2170",
            "BlackElo": "2689"
        }
    }
}
```

### Show the help

```
python test_generator.py --help
```

## Credits

* Uri Blass  
This training system is suggested by Uri in [talkchess forum](http://talkchess.com/forum3/viewtopic.php?f=2&t=80593).
* [Python chess](https://python-chess.readthedocs.io/en/latest/)
* [streamlit](https://streamlit.io/)
