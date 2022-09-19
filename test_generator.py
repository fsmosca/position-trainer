"""
Generates test positions in json format.

Installation:
  pip install chess
"""


import json
from pathlib import Path
import argparse

import chess.engine
import chess.pgn


def score_proba(score_cp):
    K = 6
    score_p = score_cp/100
    return 1 / (1 + 10 **(-score_p/K))


def build_test_info(board, epd, game_move_san, game_score_cp, game_score_rate,
                    engine_move_san, engine_score_cp, engine_score_rate,
                    user_moves, ev, da, rnd, wp, bp, wr, br,
                    engine_id_name, movetime, depth):
    return {epd: {'stm': 'white' if board.turn else 'black',
                    'fmvn': board.fullmove_number,
                    'hmvc': board.halfmove_clock,
                    'game': {'move': game_move_san,
                             'score': game_score_cp,
                             'rate': game_score_rate},
                    'engine': {'move': engine_move_san,
                               'score': engine_score_cp,
                               'rate': engine_score_rate},
                    'user': user_moves,
                    'analysis_engine': engine_id_name, 
                    'analysis_movetime': movetime, 
                    'analysis_depth': depth, 
                    'header': {'Event': ev, 'Date': da,
                                'Round': rnd, 'White': wp,
                                'Black': bp, 'WhiteElo': wr,
                                'BlackElo': br}}}


def generate_test_positions(pgn_file, engine_file, outputfile='test.json', mem=128,
                            threads=1, movetime=0.1, depth=1000, startmove=12,
                            ratemargin=0.2):
    """
    Generate test positions.
    """
    movetime = max(0.1, movetime/1000)
    engine = chess.engine.SimpleEngine.popen_uci(engine_file)
    engine.configure({'Hash': mem})
    engine.configure({'Threads': threads})
    engine_id_name = engine.id['name']

    with open(pgn_file, 'r') as fp:
        while True:
            game = chess.pgn.read_game(fp)
            if game is None:
                break

            ev = game.headers['Event']
            wp = game.headers['White']
            bp = game.headers['Black']
            wr = game.headers['WhiteElo']
            br = game.headers['BlackElo']
            da = game.headers['Date']
            rnd = game.headers['Round']

            # Parse the moves.
            for node in game.mainline():
                parent_node = node.parent
                board = parent_node.board()
                move = node.move
                game_move_san = board.san(move)
                epd = board.epd()
                fmvn = board.fullmove_number

                if fmvn < startmove:
                    continue

                # Get the engine evaluation of current position.
                info = engine.analyse(board, chess.engine.Limit(
                                      time=movetime, depth=depth))
                engine_move = info['pv'][0]
                engine_move_san = board.san(engine_move)
                engine_score_cp = info['score'].relative.score(mate_score=32000)
                engine_score_rate = round(score_proba(engine_score_cp), 2)

                # Get the engine evaluation of the game move.

                # If the game move and engine move are the same, just copy the evaluation and rate.
                if engine_move_san == game_move_san:
                    game_score_cp = engine_score_cp
                    game_score_rate = engine_score_rate
                # Else evaluate the game move with the engine.
                else:
                    # The engine used must support the searchmoves command.
                    info = engine.analyse(
                        board,
                        chess.engine.Limit(time=movetime, depth=depth),
                        root_moves=[move])
                    game_score_cp = info['score'].relative.score(mate_score=32000)
                    game_score_rate = round(score_proba(game_score_cp), 2)

                # If game move is suboptimal, we will save the position to csv.
                # A suboptimal move is when the gap from engine score rate is 0.2 or more.
                # Save test position if it is still playable or score_cp >= -100.
                if engine_score_rate - game_score_rate >= ratemargin and engine_score_cp >= -100:
                    user_moves = {}

                    # Analyze all moves in this position.
                    for m in board.legal_moves:
                        info = engine.analyse(
                            board,
                            chess.engine.Limit(time=movetime, depth=depth),
                            root_moves=[m])
                        user_move = info['pv'][0]
                        user_move_san = board.san(user_move)
                        user_score_cp = info['score'].relative.score(mate_score=32000)
                        user_score_rate = round(score_proba(user_score_cp), 2)
                        user_moves.update({
                            user_move_san: {'score': user_score_cp,
                                            'rate': user_score_rate}})

                    test_info = build_test_info(
                        board, epd, game_move_san, game_score_cp,
                        game_score_rate, engine_move_san,
                        engine_score_cp, engine_score_rate,
                        user_moves, ev, da, rnd, wp, bp, wr, br,
                        engine_id_name, movetime, depth)                    

                    # Read the json file and save it with new info.
                    if Path(outputfile).exists():
                        with open(outputfile, 'r') as f:

                            # Get the dictionary from json.
                            data = json.load(f)

                            # Update the data and save back to json.
                            data.update(test_info)
                            obj = json.dumps(data, indent=4)              
                            with open(outputfile, "w") as p:
                                p.write(obj)

                    else:
                        # Save the new data in json.
                        data = {}
                        data.update(test_info)
                        obj = json.dumps(data, indent=4)                        
                        with open(outputfile, "w") as p:
                            p.write(obj)

    engine.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate test positions.')
    parser.add_argument('--pgn-file', type=str, required=True,
                        help='input pgn filename, required=True')
    parser.add_argument('--output-file', type=str, required=False,
                        default='test.json',
                        help='output file in json format, required=False, default=test.json')
    parser.add_argument('--engine-file', type=str, required=True,
                        help='input engine filename, required=True')
    parser.add_argument('--engine-hash-mb', type=int, required=False,
                        default=128,
                        help='engine hash value in MB, required=False, default=128')
    parser.add_argument('--engine-threads', type=int, required=False,
                        default=1,
                        help='engine number of threads to use, required=False, default=1')
    parser.add_argument('--movetime', type=int, required=False,
                        default=500,
                        help='engine analysis movetime in milliseconds, required=false, default=500')
    parser.add_argument('--depth', type=int, required=False,
                        default=1000,
                        help='engine analysis search depth, required=False, default=1000')
    parser.add_argument('--start-move', type=int, required=False,
                        default=12,
                        help='analysis will be started on this move number, required=False, default=12')
    parser.add_argument('--min-error-margin', type=float, required=False,
                        default=0.2,
                        help='the minimum expected score rate margin to save the position, required=false, default=0.2')

    args = parser.parse_args()
    generate_test_positions(args.pgn_file, args.engine_file,
                            outputfile=args.output_file, mem=args.engine_hash_mb,
                            threads=args.engine_threads, movetime=args.movetime,
                            depth=args.depth, startmove=args.start_move,
                            ratemargin=args.min_error_margin)
