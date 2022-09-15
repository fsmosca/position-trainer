import chess.engine
import streamlit as st


def score_proba(score_cp):
    K = 6
    score_p = score_cp/100
    return 1 / (1 + 10 **(-score_p/K))


def analyze(fp, engine_file, anatime_sec, maxdepth, start_move_num, submit):
    cnt = 0
    if fp is not None and len(st.session_state.games) < 1 and submit:
        with st.spinner('Analyzing ...'):
            movetime_sec = anatime_sec
            efile = engine_file
            engine = chess.engine.SimpleEngine.popen_uci(efile)

            while True:
                game = chess.pgn.read_game(fp)
                if game is None:
                    break

                wp = game.headers['White']
                bp = game.headers['Black']
                wr = game.headers['WhiteElo']
                br = game.headers['BlackElo']
                da = game.headers['Date']

                for node in game.mainline():
                    parent_node = node.parent
                    board = parent_node.board()
                    move = node.move
                    game_move_san = board.san(move)
                    fen = board.fen()
                    fmvn = board.fullmove_number

                    if fmvn < start_move_num:
                        continue

                    # Engine evaluation of current position.
                    info = engine.analyse(board, chess.engine.Limit(time=movetime_sec, depth=maxdepth))
                    engine_move = info['pv'][0]
                    engine_move_san = board.san(engine_move)
                    engine_score_cp = info['score'].relative.score(mate_score=32000)
                    engine_score_rate = round(score_proba(engine_score_cp), 2)

                    # Engine evaluation of game move.
                    if engine_move_san == game_move_san:
                        game_score_cp = engine_score_cp
                        game_score_rate = engine_score_rate
                    else:
                        info = engine.analyse(board, chess.engine.Limit(time=movetime_sec), root_moves=[move])
                        game_score_cp = info['score'].relative.score(mate_score=32000)
                        game_score_rate = round(score_proba(game_score_cp), 2)

                    # If game move is suboptimal, margin is 0.2 score rate.
                    rate_margin = 0.2
                    if engine_score_rate - game_score_rate >= rate_margin:
                        st.session_state.games.update({cnt: [fen, game_move_san,
                                                                game_score_cp, game_score_rate,
                                                                engine_move_san, engine_score_cp,
                                                                engine_score_rate, wp, bp, wr, br, da]})
                        cnt += 1

            engine.quit()
            st.success(f'Game analysis is done. There are {cnt} positions saved.')
