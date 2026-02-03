import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- Supabaseの初期設定 ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- クイズのデータ設定 ---
QUIZ_DATA = [
    {"exercise": "ベンチプレス", "options": ["大胸筋", "広背筋", "大腿四頭筋", "三角筋"], "answer": "大胸筋"},
    {"exercise": "スクワット", "options": ["腹直筋", "大腿四頭筋", "上腕三頭筋", "広背筋"], "answer": "大腿四頭筋"},
    {"exercise": "デッドリフト", "options": ["大胸筋", "脊柱起立筋/ハムストリングス", "側腹筋", "僧帽筋"], "answer": "脊柱起立筋/ハムストリングス"},
    {"exercise": "ラットプルダウン", "options": ["広背筋", "大腿筋膜張筋", "下腿三頭筋", "腹斜筋"], "answer": "広背筋"},
    {"exercise": "サイドレイズ", "options": ["大胸筋", "三角筋中部", "前脛骨筋", "上腕二頭筋"], "answer": "三角筋中部"},
]

st.title("💪 筋トレ部位当てクイズ！")
st.write("種目に対して、主に鍛えられる筋肉を選択してください。結果はデータベースに保存されます。")

# --- セッション状態の初期化 ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# ユーザー名入力（最初の1回だけ）
if not st.session_state.user_name:
    name = st.text_input("あなたの名前を入力してください（ランキング用）:")
    if st.button("クイズ開始"):
        if name:
            st.session_state.user_name = name
            st.rerun()
        else:
            st.warning("名前を入力してください。")
    st.stop()

# --- クイズ本編 ---
if st.session_state.current_q < len(QUIZ_DATA):
    q = QUIZ_DATA[st.session_state.current_q]
    
    st.subheader(f"Q{st.session_state.current_q + 1}: {q['exercise']} で主に鍛えられるのは？")
    
    with st.form(key=f"q_form_{st.session_state.current_q}"):
        choice = st.radio("選択肢:", q["options"])
        submit_button = st.form_submit_button(label="回答する")
        
        if submit_button:
            is_correct = (choice == q["answer"])
            
            # Supabaseへログを送信
            data = {
                "user_name": st.session_state.user_name,
                "exercise_name": q["exercise"],
                "is_correct": is_correct
            }
            try:
                supabase.table("quiz_logs").insert(data).execute()
            except Exception as e:
                st.error(f"データの保存に失敗しました: {e}")

            if is_correct:
                st.success("正解！✨")
                st.session_state.score += 1
            else:
                st.error(f"残念！正解は {q['answer']} でした。")
            
            st.session_state.current_q += 1
            st.button("次の問題へ")

else:
    # --- 全問終了後のリザルト ---
    st.balloons()
    st.header("クイズ終了！")
    st.write(f"{st.session_state.user_name}さんのスコア: {st.session_state.score} / {len(QUIZ_DATA)}")
    
    if st.button("もう一度挑戦する"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.rerun()

    # --- 保存されたデータの表示 (Supabaseから取得) ---
    st.divider()
    st.subheader("📊 みんなの学習履歴 (Supabaseから取得)")
    
    try:
        response = supabase.table("quiz_logs").select("*").order("created_at", desc=True).limit(10).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            # 見やすく加工
            df = df[['user_name', 'exercise_name', 'is_correct', 'created_at']]
            df.columns = ['ユーザー', '種目', '正解？', '日時']
            st.table(df)
        else:
            st.info("まだ履歴がありません。")
    except Exception as e:
        st.error(f"データの取得に失敗しました: {e}")
