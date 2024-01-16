import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# Firebaseの初期化
if not firebase_admin._apps:
    cred = credentials.Certificate("./donguri-22fdb-firebase-adminsdk-ztyat-41dc93f768.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Streamlitのレイアウトを定義
st.title('どんぐりデータベースのメンテ')

# ドキュメントを検索する機能
st.subheader('検索')
with st.form('検索フォーム'):
    search_en = st.text_input('英語を入力してください')
    search_submitted = st.form_submit_button('実行')
    if search_submitted and search_en:
        docs = db.collection('en2kana_db').where('en', '==', search_en).stream()
        data = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['doc_id'] = doc.id
            data.append(doc_data)
        df = pd.DataFrame(data)
        st.write(df)

# ドキュメントを追加する機能
st.subheader('追加')
with st.form('追加フォーム'):
    en = st.text_input('英語を入力してください')
    kana = st.text_input('かな表現を入力してください')
    submitted = st.form_submit_button('実行')
    if submitted and en and kana:
        db.collection('en2kana_db').add({'en': en, 'kana': kana})
        st.success('Document added successfully!')


# ドキュメントを更新する機能
st.subheader('更新')
with st.form('更新フォーム'):
    doc_id = st.text_input('ドキュメントIDを入力してください')
    new_en = st.text_input('英語を入力してください')
    new_kana = st.text_input('かな表現を入力してください')
    update_submitted = st.form_submit_button('実行')
    if update_submitted and doc_id:
        updates = {}
        if new_en:
            updates['en'] = new_en
        if new_kana:
            updates['kana'] = new_kana
        if updates:
            db.collection('en2kana_db').document(doc_id).update(updates)
            st.success('Document updated successfully!')
