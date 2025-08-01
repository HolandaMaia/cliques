import streamlit as st
import pyautogui
import threading
import time

# Inicializa estados no session_state
if "clicking" not in st.session_state:
    st.session_state.clicking = False
if "click_thread" not in st.session_state:
    st.session_state.click_thread = None
if "stop_event" not in st.session_state:
    st.session_state.stop_event = threading.Event()

def click_loop(stop_event):
    while not stop_event.is_set():
        pyautogui.click()
        time.sleep(0.5)

st.title("Auto Clicker com Streamlit")

# Toggle de controle
toggle = st.toggle("Ativar clique automático", value=st.session_state.clicking)

# Ativar clique automático
if toggle and not st.session_state.clicking:
    st.session_state.stop_event.clear()
    thread = threading.Thread(target=click_loop, args=(st.session_state.stop_event,), daemon=True)
    thread.start()
    st.session_state.click_thread = thread
    st.session_state.clicking = True
    st.success("Clique automático iniciado!")

# Desativar clique automático
elif not toggle and st.session_state.clicking:
    st.session_state.stop_event.set()
    st.session_state.clicking = False
    st.warning("Clique automático parado.")
