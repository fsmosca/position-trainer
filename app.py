import json

import streamlit as st
from library.upload import upload_file
import chess.pgn
import chess.svg
import chess
import base64
import pandas as pd
from library.perf import expected_rating_diff


st.set_page_config(
    page_title="Position Trainer",
    page_icon="🧊",
    layout="wide"
)


if 'games' not in st.session_state:
    st.session_state.games = {}
if 'loadpos' not in st.session_state:
    st.session_state.loadpos = False
if 'posnum' not in st.session_state:
    st.session_state.posnum = 0
if 'maxpos' not in st.session_state:
    st.session_state.maxpos = 0
if 'selmove_from' not in st.session_state:
    st.session_state.selmove_from = None
if 'selmove_to' not in st.session_state:
    st.session_state.selmove_to = None
if 'user_perf_rating' not in st.session_state:
    st.session_state.user_perf_rating = []


analysis_sec = 1.0
engine_file = 'engine/sf15.exe'  # Todo: load by button


def render_svg(svg, turn):
    """Renders the given svg string."""
    stm = 'White' if turn else 'Black'
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    
    html += '<p></p>'
    html += f'Side to move: <span style="color:blue;"><strong>{stm}</strong></span><br>'
    html += f'Rating Range: <span style="color:red;"><strong>{st.session_state.minrating} - {st.session_state.maxrating}</strong></span>'
    st.write(html, unsafe_allow_html=True)


def reset_perf():
    st.session_state.user_perf_rating = []


def increment():
    st.session_state.selmove_from = None
    st.session_state.selmove_to = None
    st.session_state.posnum += 1
    if st.session_state.posnum >= st.session_state.maxpos:
        st.session_state.posnum = 0


def update_board_arrow(board):
    sanmove = st.session_state.key_selmove
    if sanmove == 'Select a move':
        st.session_state.selmove_from = None
        st.session_state.selmove_to = None
    else:
        pcmove = board.parse_san(sanmove)
        st.session_state.selmove_from = pcmove.from_square
        st.session_state.selmove_to = pcmove.to_square


def main():
    tab1, tab2, tab3, tab4 = st.tabs(['Home', 'Load Test Positions', 'Evaluation', 'Setting'])

    with tab1:
        cols = st.columns([1, 2, 1])
        with cols[1]:
            st.markdown('''
            ### Training idea

            The training positions are from the actual games where a player has played
            a suboptimal move. You will be tested if you can find a better move as strong
            as the engine move or better than the move played in the actual game.

            The idea is from Uri Blass from [talkchess forum](https://www.talkchess.com/forum3/viewtopic.php?f=2&t=80593).
            Some features are not yet implemented, like rating selection and a timer.

            ### Download

            You can download the training positions from the github repository or from google drive.
            * [github](https://github.com/fsmosca/position-trainer/tree/main/data)  
            * [google drive](https://drive.google.com/drive/folders/1Epmc0EXAldKRJ41IaW9dOWEg3OO-uvgc)

            ### Generate training positions

            You can generate a training positions using the **test_generator.py** program that can be found in
            the [github repository](https://github.com/fsmosca/position-trainer). The guide on how to run it
            is also in that repository.
            ''')
    
    with tab2:
        cols = st.columns([1, 3, 1])
        with cols[1]:
            fp = None
            with st.expander('Upload json test file'):
                st.number_input('Minimum Rating', 1000, 5000, 1500, step=5, key='minrating')
                st.number_input('Maximum Rating', 1100, 5000, 5000, step=5, key='maxrating')

                fp = upload_file()
                if fp is not None:
                    data = json.load(fp)

                    cnt = 0
                    for epd, v in data.items():
                        stm = v['stm']
                        prating = v['header']['WhiteElo'] if stm == 'white' else v['header']['BlackElo']
                        if prating != '?':
                            prating = int(prating)
                            if prating >= st.session_state.minrating and prating <= st.session_state.maxrating:
                                st.session_state.games.update({cnt: [epd, data[epd]]})
                                cnt += 1
                else:
                    st.session_state.games = {}
                    st.session_state.posnum = 0

                st.write(f'numpos {len(st.session_state.games)}')
                    
    with tab3:
        if len(st.session_state.games) == 0:
            st.warning('There are no test positions loaded, go to the Load Test Positions page.')

        # Display the fen, board and legal moves.
        if len(st.session_state.games):
            st.session_state.maxpos = len(st.session_state.games)

            cols = st.columns([1, 2])

            with cols[1]:
                c = st.session_state.posnum
                loadpos = st.button('Load Next', key='key_loadpos', on_click=increment)
                if loadpos or st.session_state.loadpos:
                    st.session_state.loadpos = loadpos
                    c = st.session_state.posnum

            fen = st.session_state.games[c][0]
            game_move_san = st.session_state.games[c][1]['game']['move']
            game_score_cp = st.session_state.games[c][1]['game']['score']
            game_score_rate = st.session_state.games[c][1]['game']['rate']
            engine_move_san = st.session_state.games[c][1]['engine']['move']
            engine_score_cp = st.session_state.games[c][1]['engine']['score']
            engine_score_rate = st.session_state.games[c][1]['engine']['rate']
            
            wp = st.session_state.games[c][1]['header']['White']
            bp = st.session_state.games[c][1]['header']['Black']
            wr = st.session_state.games[c][1]['header']['WhiteElo']
            br = st.session_state.games[c][1]['header']['BlackElo']
            da = st.session_state.games[c][1]['header']['Date']
            event = st.session_state.games[c][1]['header']['Event']

            board = chess.Board(fen)
            turn = board.turn

            opp_rating = st.session_state.games[c][1]['header']['BlackElo' if turn else 'WhiteElo']

            with cols[0]:
                if st.session_state.selmove_from is not None:
                    arrow = [chess.svg.Arrow(st.session_state.selmove_from,
                                             st.session_state.selmove_to)]
                else:
                    arrow = []

                svg_board = chess.svg.board(
                    board,
                    size=st.session_state.board_width,
                    orientation=turn,
                    arrows=arrow
                )
                render_svg(svg_board, board.turn)

            # Display the legal move for selection.
            board_legal_moves = list(board.legal_moves)  # python chess format
            legal_moves_san = [board.san(m) for m in board_legal_moves]
            legal_moves_san = sorted(legal_moves_san)
            legal_moves_san.insert(0, 'Select a move')

            with cols[1]:
                with st.expander('Position info'):
                    st.markdown(f'''
                    **PosNum: {st.session_state.posnum + 1}**  
                    **{fen}**  
                    **{wp} {wr}  - {bp} {br}**  
                    **{event}, {da}**
                    ''')

                # st.button('Legal moves', disabled=True, key='key_legalmoves')
                with st.expander('Select a move', expanded=False):
                    sel_move_san = st.radio('', options=legal_moves_san,
                    horizontal=True,
                    on_change=update_board_arrow,
                    args=[board],
                    key='key_selmove')

            sel_move_san = st.session_state.key_selmove

            if sel_move_san != 'Select a move':
                # Analyze the sel move with the engine.
                if sel_move_san == engine_move_san:
                    sel_score_cp = engine_score_cp
                    sel_score_rate = engine_score_rate
                elif sel_move_san == game_move_san:
                    sel_score_cp = game_score_cp
                    sel_score_rate = game_score_rate
                else:
                    c = st.session_state.posnum
                    sel_score_cp = st.session_state.games[c][1]['user'][sel_move_san]['score']
                    sel_score_rate = st.session_state.games[c][1]['user'][sel_move_san]['rate']

                with cols[1]:
                    resdata = {
                        'Category': ['Selected', 'Game', 'Engine'],
                        'Move': [sel_move_san, game_move_san, engine_move_san],
                        'ScoreCP': [sel_score_cp, game_score_cp, engine_score_cp],
                        'ScoreRate': [sel_score_rate, game_score_rate, engine_score_rate]
                    }

                    with st.expander('RESULT SUMMARY', expanded=True):
                        dfres = pd.DataFrame(resdata)
                        st.dataframe(dfres)

                    with st.expander('ASSESSMENT', expanded=True):
                        game_player = wp if board.turn else bp
                        player_rating = wr if board.turn else br
                        if sel_score_cp >= engine_score_cp:
                            st.write(f'You played like an engine and better than {game_player} ({player_rating})!!')
                        elif sel_score_cp > game_score_cp:
                            st.write(f'You played better than {game_player} ({player_rating})!')
                        elif sel_score_cp < game_score_cp:
                            st.write(f'You played below the level of {game_player} ({player_rating}).')
                        else:
                            st.write(f'You played the same level as {game_player} ({player_rating})')

                    with st.expander('PERFORMANCE RATING'):
                        engine_rd = expected_rating_diff(engine_score_rate)
                        user_rd = expected_rating_diff(sel_score_rate)
                        if opp_rating != '?':
                            rd_diff = user_rd - engine_rd
                            st.session_state.user_perf_rating.append(int(opp_rating) + round(rd_diff))

                        average_perf = round(sum(st.session_state.user_perf_rating) / len(st.session_state.user_perf_rating))
                        st.markdown(f'''
                        User Performance Rating: <span style="color:green;"><strong>{average_perf}</strong></span>
                        ''',
                        unsafe_allow_html=True)
                        st.write(st.session_state.user_perf_rating)

    with tab4:
        cols = st.columns([1, 3, 1])

        with cols[1]:
            st.number_input('Board width', 150, 800, 400, step=50, key='board_width')
            st.button('Reset performance Rating', key='k_reset_perf', on_click=reset_perf,
                       help='Press the "Load Next" button first in the Evaluation tab, before pressing this reset.')


if __name__ == '__main__':
    main()
