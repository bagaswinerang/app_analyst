import streamlit as st
import pandas as pd
from openai import OpenAI
import io

# =========================
# Setup OpenRouter Client
# =========================
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["api_key"],
)

st.set_page_config(page_title="📊 Sales Analysis with LLM", layout="wide")
st.title("📊 Sales Analysis with LLM")

# =========================
# Upload CSV
# =========================
uploaded_file = st.file_uploader("📂 Upload CSV data kamu", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Data Preview")
    st.dataframe(df)

    # =========================
    # Session State Initialization
    # =========================
    if "data_original" not in st.session_state:
        st.session_state["data_original"] = df.copy()
    if "data_modified" not in st.session_state:
        st.session_state["data_modified"] = df.copy()
    if "data_previous" not in st.session_state:
        st.session_state["data_previous"] = df.copy()

    df_current = st.session_state["data_modified"]

    # =========================
    # Tambah Kolom Manual
    # =========================
    st.subheader("🛠 Tambahkan Kolom Baru Manual")
    new_col_name = st.text_input("Nama Kolom Baru")
    col_formula = st.text_area("Formula (contoh: df['Units Sold'] * df['Price'] untuk Revenue)")

    if st.button("Generate Kolom Baru", key="add_col"):
        if new_col_name and col_formula:
            try:
                st.session_state["data_previous"] = df_current.copy()
                df_current[new_col_name] = eval(col_formula)
                st.session_state["data_modified"] = df_current.copy()
                st.success(f"Kolom '{new_col_name}' berhasil ditambahkan!")
            except Exception as e:
                st.error(f"Ada error saat generate kolom: {e}")
        else:
            st.warning("Isi nama kolom dan formula terlebih dahulu!")

    # =========================
    # Hapus Kolom
    # =========================
    st.subheader("🗑 Hapus Kolom")
    col_to_delete = st.selectbox("Pilih kolom untuk dihapus", options=df_current.columns)
    if st.button("Hapus Kolom", key="delete_col"):
        try:
            st.session_state["data_previous"] = df_current.copy()
            df_current = df_current.drop(columns=[col_to_delete])
            st.session_state["data_modified"] = df_current.copy()
            st.success(f"Kolom '{col_to_delete}' berhasil dihapus!")
        except Exception as e:
            st.error(f"Ada error saat menghapus kolom: {e}")

    # =========================
    # Reset ke Data Awal
    # =========================
    if st.button("🔄 Reset ke Data Awal"):
        df_current = st.session_state["data_original"].copy()
        st.session_state["data_modified"] = df_current.copy()
        st.session_state["data_previous"] = df_current.copy()
        st.success("Data berhasil dikembalikan ke kondisi awal!")

    # =========================
    # Undo
    # =========================
    if st.button("↩️ Undo Perubahan Terakhir", key="undo"):
        if "data_previous" in st.session_state:
            df_current = st.session_state["data_previous"].copy()
            st.session_state["data_modified"] = df_current.copy()
            st.success("Perubahan terakhir berhasil di-undo!")
        else:
            st.warning("Tidak ada perubahan untuk di-undo!")

    # =========================
    # Tampilkan Data CSV Terbaru
    # =========================
    st.subheader("📄 Data CSV Terbaru")
    st.dataframe(df_current)

    # =========================
    # Download CSV terbaru
    # =========================
    st.subheader("💾 Download CSV Terbaru")
    csv_buffer = io.StringIO()
    df_current.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download CSV",
        data=csv_buffer.getvalue(),
        file_name="data_modified.csv",
        mime="text/csv"
    )

    # =========================
    # Statistik Deskriptif
    # =========================
    st.subheader("📊 Statistik Deskriptif")
    st.dataframe(df_current.describe(include='all'))

    # =========================
    # Chat Interaktif
    # =========================
    st.subheader("💬 Chat dengan AI Analyst")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": "You are a helpful data analyst assistant."},
            {"role": "assistant", "content": "Halo! Saya siap membantu analisis data kamu. Apa yang ingin kamu tanyakan tentang dataset ini?"}
        ]

    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if user_input := st.chat_input("Tanyakan sesuatu tentang data kamu..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        full_prompt = f"""
Berikut adalah dataset CSV:
{df_current.to_csv(index=False)}
Pertanyaan user: {user_input}
"""

        with st.spinner("AI sedang menganalisis..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful data analyst assistant."},
                    {"role": "user", "content": full_prompt},
                ],
            )

        ai_reply = response.choices[0].message.content
        st.session_state["messages"].append({"role": "assistant", "content": ai_reply})
        st.chat_message("assistant").write(ai_reply)