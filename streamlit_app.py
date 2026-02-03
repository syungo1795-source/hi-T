import streamlit as st
from supabase import create_client, Client
import pandas as pd
import random

# --- Supabaseの初期設定 ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- クイズのデータ（全30問） ---
TOTAL_QUIZ_DATA = [
    {"exercise": "ベンチプレス", "options": ["大胸筋", "広背筋", "大腿四頭筋", "三角筋"], "answer": "大胸筋"},
    {"exercise": "スクワット", "options": ["大腿四頭筋", "腹直筋", "上腕三頭筋", "広背筋"], "answer": "大腿四頭筋"},
    {"exercise": "デッドリフト", "options": ["脊柱起立筋/ハムストリングス", "大胸筋", "側腹筋", "僧帽筋"], "answer": "脊柱起立筋/ハムストリングス"},
    {"exercise": "ラットプルダウン", "options": ["広背筋", "大腿筋膜張筋", "下腿三頭筋", "腹斜筋"], "answer": "広背筋"},
    {"exercise": "サイドレイズ", "options": ["三角筋中部", "大胸筋", "前脛骨筋", "上腕二頭筋"], "answer": "三角筋中部"},
    {"exercise": "レッグカール", "options": ["ハムストリングス", "大腿四頭筋", "腓腹筋", "大胸筋"], "answer": "ハムストリングス"},
    {"exercise": "アームカール", "options": ["上腕二頭筋", "上腕三頭筋", "前腕筋", "三角筋後部"], "answer": "上腕二頭筋"},
    {"exercise": "フレンチプレス", "options": ["上腕三頭筋", "上腕二頭筋", "大円筋", "菱形筋"], "answer": "上腕三頭筋"},
    {"exercise": "チンニング（懸垂）", "options": ["広背筋", "大胸筋", "腹直筋", "大腿筋膜張筋"], "answer": "広背筋"},
    {"exercise": "ブルガリアンスクワット", "options": ["大臀筋/大腿四頭筋", "広背筋", "三角筋", "脊柱起立筋"], "answer": "大臀筋/大腿四頭筋"},
    {"exercise": "ショルダープレス", "options": ["三角筋前部/中部", "僧帽筋", "広背筋", "腹斜筋"], "answer": "三角筋前部/中部"},
    {"exercise": "クランチ", "options": ["腹直筋", "広背筋", "下腿三頭筋", "上腕三頭筋"], "answer": "腹直筋"},
    {"exercise": "レッグエクステンション", "options": ["大腿四頭筋", "ハムストリングス", "大臀筋", "内転筋"], "answer": "大腿四頭筋"},
    {"exercise": "カーフレイズ", "options": ["下腿三頭筋（ふくらはぎ）", "前脛骨筋", "大腿四頭筋", "腹直筋"], "answer": "下腿三頭筋（ふくらはぎ）"},
    {"exercise": "ハンマーカール", "options": ["上腕二頭筋/腕橈骨筋", "上腕三頭筋", "広背筋", "三角筋後部"], "answer": "上腕二頭筋/腕橈骨筋"},
    {"exercise": "フェイスプル", "options": ["三角筋後部/棘下筋", "大胸筋", "腹直筋", "大腿四頭筋"], "answer": "三角筋後部/棘下筋"},
    {"exercise": "プランク", "options": ["腹直筋/体幹", "上腕二頭筋", "大腿四頭筋", "僧帽筋"], "answer": "腹直筋/体幹"},
    {"exercise": "ヒップスラスト", "options": ["大臀筋", "腹直筋", "広背筋", "三角筋"], "answer": "大臀筋"},
    {"exercise": "ベントオーバーロウ", "options": ["広背筋/背中", "大胸筋", "腹直筋", "大腿四頭筋"], "answer": "広背筋/背中"},
    {"exercise": "チェストフライ", "options": ["大胸筋", "広背筋", "三角筋後部", "上腕三頭筋"], "answer": "大胸筋"},
    {"exercise": "ランジ", "options": ["大腿四頭筋/大臀筋", "僧帽筋", "前腕筋", "脊柱起立筋"], "answer": "大腿四頭筋/大臀筋"},
    {"exercise": "レッグプレス", "options": ["大腿四頭筋/大臀筋", "広背筋", "腹直筋", "三角筋"], "answer": "大腿四頭筋/大臀筋"},
    {"exercise": "ライイング・トライセプス・エクステンション", "options": ["上腕三頭筋", "上腕二頭筋", "腹直筋", "大胸筋"], "answer": "上腕三頭筋"},
    {"exercise": "プリチャーカール", "options": ["上腕二頭筋", "三角筋", "広背筋", "大臀筋"], "answer": "上腕二頭筋"},
    {"exercise": "アップライトロウ", "options": ["三角筋/僧帽筋", "大腿四頭筋", "腹直筋", "ハムストリングス"], "answer": "三角筋/僧帽筋"},
    {"exercise": "シュラッグ", "options": ["僧帽筋", "腹直筋", "大胸筋", "大腿四頭筋"], "answer": "僧帽筋"},
    {"exercise": "リアレイズ", "options": ["三角筋後部", "三角筋前部", "大胸筋", "広背筋"], "answer": "三角筋後部"},
    {"exercise": "バイシクルクランチ", "options": ["腹斜筋/腹直筋", "広背筋", "大腿四頭筋", "三角筋"], "answer": "腹斜筋/腹直筋"},
    {"exercise": "ケーブル・プッシュダウン", "options": ["上腕三頭筋", "上腕二頭筋", "大胸筋", "広背筋"], "answer": "上腕三頭筋"},
    {"exercise": "グルートブリッジ", "options": ["大臀筋", "腹直筋", "上腕三頭筋", "大胸筋"], "answer": "大臀筋"},
]

st.title("💪 究極！筋トレ部位当てクイズ")

# --- セッション状態の初期化 ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'quiz_pool' not in st.session_state:
    st.session_state.quiz_pool = random.sample(TOTAL_QUIZ_DATA, 10)
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
# 今回のアップデート：現在の問題の「シャッフルされた選択肢」を保存する場所
if 'current_options' not in st.session_state:
    st.session_state.current_options = []

# ユーザー名入力
if not st.session_state.user_name:
    name = st.text_input("挑戦者の名前を入力:")
    if st.button("クイズ開始"):
        if name:
            st.session_state.user_name = name
            st.rerun()
        else:
            st.warning("名前を入力してください。")
    st.stop()

# --- クイズ本編 ---
quiz_items = st.session_state.quiz_pool

if st.session_state.current_q < len(quiz_items):
    q = quiz_items[st.session_state.current_q]
    
    # 選択肢をシャッフル（まだ今問の選択肢が決まっていない場合のみ実行）
    if not st.session_state.current_options:
        shuffled = random.sample(q["options"], len(q["options"]))
        st.session_state.current_options = shuffled

    # 進捗表示
    st.progress((st.session_state.current_q) / len(quiz_items))
    st.write(f"問題 {st.session_state.current_q + 1} / {len(quiz_items)}")

    st.subheader(f"Q: **{q['exercise']}** で主に鍛えられるのは？")
    
    with st.form(key=f"q_form_{st.session_state.current_q}"):
        # 保存しておいたシャッフル済み選択肢を表示
        choice = st.radio("正しい筋肉はどれ？", st.session_state.current_options)
        submit_button = st.form_submit_button(label="回答を送信")
        
        if submit_button:
            is_correct = (choice == q["answer"])
            # Supabaseへ保存
            try:
                data = {"user_name": st.session_state.user_name, "exercise_name": q["exercise"], "is_correct": is_correct}
                supabase.table("quiz_logs").insert(data).execute()
            except:
                pass
            
            if is_correct:
                st.success("正解！お見事です！✨")
                st.session_state.score += 1
            else:
                st.error(f"不正解...。正解は **{q['answer']}** でした。")
            st.session_state.answered = True

    if st.session_state.answered:
        if st.button("次の問題へ ➡️"):
            st.session_state.current_q += 1
            st.session_state.answered = False
            # 次の問題のために選択肢をリセット
            st.session_state.current_options = []
            st.rerun()

else:
    # --- クイズ終了 ---
    st.balloons()
    st.header("🏁 クイズ終了！")
    st.write(f"{st.session_state.user_name}さんの最終スコア: **{st.session_state.score} / {len(quiz_items)}**")
    
    if st.button("新しい問題に挑戦する（10問）"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.quiz_pool = random.sample(TOTAL_QUIZ_DATA, 10)
        st.session_state.current_options = []
        st.rerun()

    # 履歴表示
    st.divider()
    st.subheader("📊 みんなの最新の回答履歴")
    try:
        res = supabase.table("quiz_logs").select("*").order("created_at", desc=True).limit(5).execute()
        if res.data:
            df = pd.DataFrame(res.data)
            df['結果'] = df['is_correct'].apply(lambda x: "✅正解" if x else "❌不正解")
            st.table(df[['user_name', 'exercise_name', '結果']].rename(columns={'user_name':'名前','exercise_name':'種目'}))
    except:
        st.info("データの取得に失敗しました。")
