import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- Supabaseの初期設定 ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- クイズのデータ（12問に増量！） ---
QUIZ_DATA = [
    {"exercise": "ベンチプレス", "options": ["大胸筋", "広背筋", "大腿四頭筋", "三角筋"], "answer": "大胸筋"},
    {"exercise": "スクワット", "options": ["腹直筋", "大腿四頭筋", "上腕三頭筋", "広背筋"], "answer": "大腿四頭筋"},
    {"exercise": "デッドリフト", "options": ["大胸筋", "脊柱起立筋/ハムストリングス", "側腹筋", "僧帽筋"], "answer": "脊柱起立筋/ハムストリングス"},
    {"exercise": "ラットプルダウン", "options": ["広背筋", "大腿筋膜張筋", "下腿三頭筋", "腹斜筋"], "answer": "広背筋"},
    {"exercise": "サイドレイズ", "options": ["大胸筋", "三角筋中部", "前脛骨筋", "上腕二頭筋"], "answer": "三角筋中部"},
    {"exercise": "レッグカール", "options": ["大腿四頭筋", "ハムストリングス", "腓腹筋", "大胸筋"], "answer": "ハムストリングス"},
    {"exercise": "アームカール", "options": ["上腕三頭筋", "上腕二頭筋", "前腕筋", "三角筋後部"], "answer": "上腕二頭筋"},
    {"exercise": "フレンチプレス", "options": ["上腕二頭筋", "上腕三頭筋", "大円筋", "菱形筋"], "answer": "上腕三頭筋"},
    {"exercise": "チンニング（懸垂）", "options": ["広背筋", "大胸筋", "腹直筋", "大腿筋膜張筋"], "answer": "広背筋"},
    {"exercise": "ブルガリアンスクワット", "options": ["大臀筋/大腿四頭筋", "広背筋", "三角筋", "脊柱起立筋"], "answer": "大臀筋/大腿四頭筋"},
    {"exercise": "ショルダープレス", "options": ["僧帽筋", "三角筋前部/中部", "広背筋", "腹斜筋"], "answer": "三角筋前部/中部"},
    {"exercise": "クランチ", "options": ["腹直筋", "広背筋", "下腿三頭筋", "上腕三頭筋"], "answer": "腹直筋"},
]

st.title("💪 筋トレ部位当てマスタークイズ！")

# --- セッション状態の初期化 ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'answered' not in st.session_state:
    st.session_state.answered = False

# ユーザー名入力
if not st.session_state.user_name:
    name = st.text_input("ランキングに登録する名前を入力してください:")
    if st.button("クイズ開始！"):
        if name:
            st.session_state.user_name = name
            st.rerun()
        else:
            st.warning("名前を入力してください。")
    st.stop()

# --- クイズ本編 ---
if st.session_state.current_q < len(QUIZ_DATA):
    q = QUIZ_DATA[st.session_state.current_q]
    
    # プログレスバー（進捗状況）の表示
    progress = (st.session_state.current_q) / len(QUIZ_DATA)
    st.progress(progress)
    st.write(f"進行状況: {st.session_state.current_q + 1} / {len(QUIZ_DATA)}")

    st.subheader(f"Q{st.session_state.current_q + 1}: **{q['exercise']}** で主に鍛えられるのは？")
    
    with st.form(key=f"q_form_{st.session_state.current_q}"):
        choice = st.radio("正しい筋肉を選択してください:", q["options"])
        submit_button = st.form_submit_button(label="回答を確定する")
        
        if submit_button:
            is_correct = (choice == q["answer"])
            
            # Supabaseへ回答を記録
            try:
                data = {
                    "user_name": st.session_state.user_name,
                    "exercise_name": q["exercise"],
                    "is_correct": is_correct
                }
                supabase.table("quiz_logs").insert(data).execute()
            except Exception:
                pass # エラー時は無視して進める
            
            if is_correct:
                st.success("正解！さすがです！✨")
                st.session_state.score += 1
            else:
                st.error(f"残念...。正解は **{q['answer']}** でした。")
            st.session_state.answered = True

    # フォームの外に「次へ」ボタンを配置
    if st.session_state.answered:
        if st.button("次の問題へ ➡️"):
            st.session_state.current_q += 1
            st.session_state.answered = False
            st.rerun()

else:
    # --- クイズ終了後の表示 ---
    st.balloons()
    st.header("🎉 全問終了！")
    
    # 評価コメント
    score_rate = st.session_state.score / len(QUIZ_DATA)
    if score_rate == 1.0:
        comment = "完璧です！あなたは筋トレマスター！🥇"
    elif score_rate >= 0.7:
        comment = "素晴らしい！かなり詳しいですね！🥈"
    else:
        comment = "ナイスファイト！次は全問正解を目指しましょう！🥉"
        
    st.subheader(f"{st.session_state.user_name}さんの結果")
    st.write(f"スコア: **{st.session_state.score}** / {len(QUIZ_DATA)}")
    st.info(comment)
    
    if st.button("もう一度最初から挑戦する"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.rerun()

    # --- 履歴の表示（Supabaseから読み取り） ---
    st.divider()
    st.subheader("📊 みんなの最近の回答状況")
    try:
        res = supabase.table("quiz_logs").select("*").order("created_at", desc=True).limit(10).execute()
        if res.data:
            log_df = pd.DataFrame(res.data)
            # 正誤をアイコンに変換して見やすくする
            log_df['結果'] = log_df['is_correct'].apply(lambda x: "✅ 正解" if x else "❌ 不正解")
            st.table(log_df[['user_name', 'exercise_name', '結果']].rename(columns={'user_name': '名前', 'exercise_name': '種目'}))
    except:
        st.write("履歴の読み込みに失敗しました。")
