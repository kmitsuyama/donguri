import streamlit as st
import sqlite3
import pandas as pd

# データベース接続を確立する関数
def create_connection(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        st.error(e)
    return conn

# レコードを検索する関数
def search_records(conn, en):
    query = "SELECT * FROM en2kana WHERE en = ?"
    df = pd.read_sql_query(query, conn, params=(en,))
    return df

# レコードを追加する関数
def add_record(conn, en, kana):
    query = "INSERT INTO en2kana (en, kana) VALUES (?, ?)"
    try:
        conn.execute(query, (en, kana))
        conn.commit()
        st.success("レコードが追加されました")
    except sqlite3.Error as e:
        st.error(e)

# レコードを更新する関数
def update_record(conn, en, kana):
    query = "UPDATE en2kana SET kana = ? WHERE en = ?"
    try:
        conn.execute(query, (kana, en))
        conn.commit()
        st.success("レコードが更新されました")
    except sqlite3.Error as e:
        st.error(e)

# Streamlit UI
def main():
    st.title("en2kana データベース管理アプリ")

    db_path = './en2kana_db.db'
    conn = create_connection(db_path)

    if conn:
        st.subheader("レコードを検索")
        search_en = st.text_input("検索する英語の単語を入力してください:")
        if st.button("検索"):
            df = search_records(conn, search_en)
            st.write(df)

        st.subheader("レコードを追加")
        add_en = st.text_input("追加する英語の単語を入力してください:")
        add_kana = st.text_input("追加するカナを入力してください:")
        if st.button("追加"):
            add_record(conn, add_en, add_kana)

        st.subheader("レコードを更新")
        update_en = st.text_input("更新する英語の単語を入力してください:")
        update_kana = st.text_input("新しいカナを入力してください:")
        if st.button("更新"):
            update_record(conn, update_en, update_kana)

if __name__ == "__main__":
    main()
