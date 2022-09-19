import json

import streamlit as st
from library.upload import upload_pgn
import chess.pgn
import chess.svg
import chess
import base64
import pandas as pd


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


analysis_sec = 1.0
engine_file = 'engine/sf15.exe'  # Todo: load by button


def render_svg(svg, turn):
    """Renders the given svg string."""
    stm = 'White' if turn else 'Black'
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    
    html += '<p></p>'
    html += 'Side to move: ' + '<strong>' + stm + '</strong>'
    st.write(html, unsafe_allow_html=True)


def increment():
    st.session_state.posnum += 1
    if st.session_state.posnum >= st.session_state.maxpos:
        st.session_state.posnum = 0


def main():
    tab1, tab2 = st.tabs(['Load Test Positions', 'Evaluation'])
    
    with tab1:
        cols = st.columns([1, 1, 1])
        with cols[1]:
            fp = None
            with st.expander('Upload json test file'):
                fp = upload_pgn()
                if fp is not None:
                    data = json.load(fp)                    
                    keys = data.keys()

                    for i, epd in zip(range(len(data)), keys):
                        st.session_state.games.update({i: [epd, data[epd]]})

                else:
                    st.session_state.games = {}
                    st.session_state.posnum = 0

                st.write(f'numpos {len(st.session_state.games)}')
                    
    with tab2:
        if len(st.session_state.games) == 0:
            st.warning('There are no test positions generated')

        # Display the fen, board and legal moves.
        if len(st.session_state.games):
            st.session_state.maxpos = len(st.session_state.games)

            cols = st.columns([1, 2])

            with cols[0]:
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
            flipped = True if not turn else False

            with cols[0]:
                svg_board = chess.svg.board(board, size=400, flipped=flipped)
                render_svg(svg_board, board.turn)

                with st.expander('Position info'):
                    st.markdown(f'''
                    **PosNum: {st.session_state.posnum + 1}**  
                    **{fen}**  
                    **{wp} {wr}  - {bp} {br}**  
                    **{event}, {da}**
                    ''')

            # Display the legal move for selection.
            board_legal_moves = list(board.legal_moves)  # python chess format
            legal_moves_san = [board.san(m) for m in board_legal_moves]
            legal_moves_san = sorted(legal_moves_san)
            legal_moves_san.insert(0, 'Select a move')

            with cols[1]:
                st.button('Legal moves', disabled=True, key='key_legalmoves')
                with st.expander('Select a move', expanded=False):
                    sel_move_san = st.radio('', options=legal_moves_san, horizontal=True)

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

                    st.markdown('''
                    ##### Test result summary
                    ''')

                    dfres = pd.DataFrame(resdata)
                    st.dataframe(dfres)

                    with st.expander('ASSESSMENT', expanded=True):
                        game_player = wp if board.turn else bp
                        if sel_score_cp >= engine_score_cp:
                            st.write(f'You played like an engine and better than {game_player}!!')
                        elif sel_score_cp > game_score_cp:
                            st.write(f'You played better than {game_player}!')
                        elif sel_score_cp < game_score_cp:
                            st.write(f'You played below the level of {game_player}.')
                        else:
                            st.write(f'You played the same level as {game_player}')


if __name__ == '__main__':
    main()
