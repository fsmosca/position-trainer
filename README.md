# Position-Trainer
Test your skill to find the best move from the given test position where the player from the test sets fails to find. It generates a summary table with your selected move, the game move and the engine move. The test sets in json format can be found under the data folder.

You can also generate test positions with the use of `test_generator.py` which can be found in this repository. You need the [stockfish](https://stockfishchess.org/) engine to analyze the positions where the test_generator saves interesting positions in json format. There is also a stockfish 15 compiled for modern hardware under the engine folder.

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
    "1r2r2k/3bbqpp/3p4/1NpP4/2P1QP2/6P1/1B5P/1R2R1K1 w - -": {
        "stm": "white",
        "fmvn": 26,
        "hmvc": 1,
        "game": {
            "move": "Qf3",
            "score": 5,
            "rate": 0.5
        },
        "engine": {
            "move": "Nc7",
            "score": 319,
            "rate": 0.77
        },
        "user": {
            "Nc7": {
                "score": 333,
                "rate": 0.78
            },
            "Na7": {
                "score": -412,
                "rate": 0.17
            },
            "Nxd6": {
                "score": -375,
                "rate": 0.19
            },
            "Nd4": {
                "score": -602,
                "rate": 0.09
            },
            "Nc3": {
                "score": -459,
                "rate": 0.15
            },
            "Na3": {
                "score": -354,
                "rate": 0.2
            },
            "Qxh7+": {
                "score": -986,
                "rate": 0.02
            },
            "Qxe7": {
                "score": -735,
                "rate": 0.06
            },
            "Qg6": {
                "score": -1151,
                "rate": 0.01
            },
            "Qe6": {
                "score": -674,
                "rate": 0.07
            },
            "Qf5": {
                "score": -1272,
                "rate": 0.01
            },
            "Qe5": {
                "score": -893,
                "rate": 0.03
            },
            "Qd4": {
                "score": -1014,
                "rate": 0.02
            },
            "Qf3": {
                "score": 0,
                "rate": 0.5
            },
            "Qe3": {
                "score": -51,
                "rate": 0.45
            },
            "Qd3": {
                "score": -176,
                "rate": 0.34
            },
            "Qg2": {
                "score": -47,
                "rate": 0.46
            },
            "Qe2": {
                "score": -71,
                "rate": 0.43
            },
            "Qc2": {
                "score": -263,
                "rate": 0.27
            },
            "Qh1": {
                "score": -58,
                "rate": 0.44
            },
            "Bxg7+": {
                "score": -424,
                "rate": 0.16
            },
            "Bf6": {
                "score": -494,
                "rate": 0.13
            },
            "Be5": {
                "score": -345,
                "rate": 0.21
            },
            "Bd4": {
                "score": -600,
                "rate": 0.09
            },
            "Bc3": {
                "score": -133,
                "rate": 0.38
            },
            "Ba3": {
                "score": -287,
                "rate": 0.25
            },
            "Bc1": {
                "score": -700,
                "rate": 0.06
            },
            "Ba1": {
                "score": -211,
                "rate": 0.31
            },
            "Kg2": {
                "score": -194,
                "rate": 0.32
            },
            "Kf2": {
                "score": -178,
                "rate": 0.34
            },
            "Kh1": {
                "score": -241,
                "rate": 0.28
            },
            "Kf1": {
                "score": -212,
                "rate": 0.31
            },
            "Re3": {
                "score": -470,
                "rate": 0.14
            },
            "Re2": {
                "score": -504,
                "rate": 0.13
            },
            "Rf1": {
                "score": -204,
                "rate": 0.31
            },
            "Red1": {
                "score": -220,
                "rate": 0.3
            },
            "Rec1": {
                "score": -270,
                "rate": 0.26
            },
            "Rbd1": {
                "score": -34,
                "rate": 0.47
            },
            "Rbc1": {
                "score": -28,
                "rate": 0.47
            },
            "Ra1": {
                "score": -28,
                "rate": 0.47
            },
            "f5": {
                "score": -71,
                "rate": 0.43
            },
            "g4": {
                "score": -476,
                "rate": 0.14
            },
            "h3": {
                "score": -323,
                "rate": 0.22
            },
            "h4": {
                "score": -228,
                "rate": 0.29
            }
        },
        "header": {
            "Event": "Saint Louis Blitz 2022",
            "Date": "2022.08.29",
            "Round": "1.1",
            "White": "Nakamura, Hikaru",
            "Black": "Caruana, Fabiano",
            "WhiteElo": "2768",
            "BlackElo": "2776"
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
