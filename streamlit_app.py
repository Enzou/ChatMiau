import streamlit as st
from openai import OpenAI
from openai import RateLimitError, APIError, APIConnectionError, AuthenticationError

st.title("💬 Chatbot")
st.write(
    "Este es un chatbot simple que usa el modelo GPT-3.5 de OpenAI. "
    "Debes ingresar tu API Key, que puedes obtener [aquí](https://platform.openai.com/account/api-keys)."
)

openai_api_key = st.text_input("🔑 Clave API de OpenAI", type="password")

if not openai_api_key:
    st.info("Agrega tu clave de API para comenzar.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escribe tu mensaje aquí..."):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except RateLimitError:
            st.error("⚠️ Has alcanzado el límite de uso de la API de OpenAI. Espera un momento o revisa tu cuota.", icon="⏱️")
        except AuthenticationError:
            st.error("❌ Tu clave API no es válida. Verifica que la hayas copiado correctamente.", icon="🔐")
        except APIConnectionError:
            st.error("🔌 Problema de conexión con OpenAI. Verifica tu red.", icon="🌐")
        except APIError:
            st.error("🚨 Error del servidor de OpenAI. Intenta más tarde.", icon="⚙️")
        except Exception as e:
            st.error(f"❗ Error inesperado: {e}", icon="🐞")
