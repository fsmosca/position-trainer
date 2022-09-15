import streamlit as st
from library.analysis import score_proba, analyze
from library.upload import upload_pgn
import chess.pgn
import chess.svg
import chess
import base64
import pandas as pd


st.set_page_config(
    page_title="Evaluator",
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


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    html += '<p></p>'
    st.write(html, unsafe_allow_html=True)


def increment():
    st.session_state.posnum += 1
    if st.session_state.posnum >= st.session_state.maxpos:
        st.session_state.posnum = 0


def main():
    tab1, tab2 = st.tabs(['PGN file', 'Evaluation'])
    
    with tab1:
        cols = st.columns([1, 1, 1])
        with cols[1]:
            fp = None
            with st.expander('Upload pgn file'):
                fp = upload_pgn()

            with st.expander('Analyze game'):
                with st.form('analyze games'):
                    anatime_sec = st.number_input('analysis time in sec', 0.1, 60.0, 0.5, key='key_anatimesec',
                                                  help='min=0.1, max=60.0, def=0.5')
                    maxdepth = st.number_input('analysis depth', 1, 1000, 16, key='key_anadepth',
                                               help='min=1, max=1000, def=16')
                    start_move_num = st.number_input('start move number', 1, 60, 12, key='key_startmovenum')
                    submit = st.form_submit_button('analyze')

                if submit:
                    st.session_state.games = {}
                    st.session_state.posnum = 0

                analyze(fp, engine_file, anatime_sec, maxdepth, start_move_num, submit)

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
            game_move_san = st.session_state.games[c][1]
            game_score_cp = st.session_state.games[c][2]
            game_score_rate = st.session_state.games[c][3]
            engine_move_san = st.session_state.games[c][4]
            engine_score_cp = st.session_state.games[c][5]
            engine_score_rate = st.session_state.games[c][6]
            wp = st.session_state.games[c][7]
            bp = st.session_state.games[c][8]
            wr = st.session_state.games[c][9]
            br = st.session_state.games[c][10]
            da = st.session_state.games[c][11]

            board = chess.Board(fen)
            turn = board.turn
            flipped = True if not turn else False

            with cols[0]:
                svg_board = chess.svg.board(board, size=400, flipped=flipped)
                render_svg(svg_board)

                with st.expander('Position info'):
                    st.markdown(f'''
                    **PosNum: {st.session_state.posnum + 1}**  
                    **{fen}**  
                    **{wp} {wr}  - {bp} {br}, {da}**
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
                    movetime_sec = analysis_sec
                    efile = engine_file
                    engine = chess.engine.SimpleEngine.popen_uci(efile)

                    info = engine.analyse(board, chess.engine.Limit(time=movetime_sec), root_moves=[board.parse_san(sel_move_san)])
                    sel_score_cp = info['score'].relative.score(mate_score=32000)
                    sel_score_rate = round(score_proba(sel_score_cp), 2)
                    engine.quit()

                with cols[1]:
                    data = {
                        'Category': ['Selected', 'Game', 'Engine'],
                        'Move': [sel_move_san, game_move_san, engine_move_san],
                        'ScoreCP': [sel_score_cp, game_score_cp, engine_score_cp],
                        'ScoreRate': [sel_score_rate, game_score_rate, engine_score_rate]
                    }

                    dfres = pd.DataFrame(data)
                    st.dataframe(dfres)


if __name__ == '__main__':
    main()
