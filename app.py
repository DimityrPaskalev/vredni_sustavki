import streamlit as st
import easyocr
from PIL import Image
import re
import numpy as np

st.title("OCR за разпознаване на Е-та и вредни съставки")

# Вредни съставки (английски + български)
bad_ingredients = [
    "palm oil", "палмово масло",
    "E621", "E102", "E133", "E250", "E211", "E951",
    "E407", "E110", "E129",
    "E471", "E472",
    "HFCS", "глюкозо-фруктозен сироп",
    "white flour", "бяло брашно",
    "modified starch", "модифицирано нишесте",
    "artificial flavors", "изкуствени аромати",
    "E450", "E338", "E320",
    "MSM",
    "processed cheese", "топено сирене", "консерванти"
]

uploaded_file = st.file_uploader("Качи снимка", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_column_width=True)

    image_np = np.array(image)

    st.write("Разпознаване на текст...")

    reader = easyocr.Reader(['bg', 'en'])
    results = reader.readtext(image_np)

    extracted_text = " ".join([res[1] for res in results])
    extracted_text_lower = extracted_text.lower()

    st.subheader("📄 Разпознат текст:")
    st.write(extracted_text)

    # Търсене на Е-та
    e_numbers = re.findall(r'\bE\d{3,4}\b', extracted_text.upper())

    # Търсене на вредни съставки
    found_bad = []
    for ingredient in bad_ingredients:
        if ingredient.lower() in extracted_text_lower:
            found_bad.append(ingredient)

    st.subheader("🧪 Открити Е-та:")
    if e_numbers:
        for e in set(e_numbers):
            st.write(f"- {e}")
    else:
        st.write("Не са открити Е-та.")

    st.subheader("⚠️ Вредни съставки:")
    if found_bad:
        for item in set(found_bad):
            st.error(f"Открито: {item}")
    else:
        st.success("Няма открити вредни съставки.")
