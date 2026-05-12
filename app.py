# Streamlit приложение за OCR и разпознаване на вредни съставки

## app.py

```python
import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import cv2
import re

# --------------------------------------------------
# Настройки на страницата
# --------------------------------------------------
st.set_page_config(
    page_title="OCR Проверка на съставки",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Проверка на вредни съставки")
st.write(
    "Качи снимка или направи снимка с камерата, "
    "за да разпознаеш текст и да провериш за вредни съставки."
)

# --------------------------------------------------
# Списък с вредни съставки
# --------------------------------------------------
HARMFUL_INGREDIENTS = {
    "e621": "Мононатриев глутамат (MSG)",
    "monosodium glutamate": "Мононатриев глутамат (MSG)",
    "palm oil": "Палмово масло",
    "palmolein": "Палмово масло",
    "hydrogenated oil": "Хидрогенирано масло",
    "aspartame": "Аспартам",
    "sodium nitrite": "Натриев нитрит",
    "e250": "Натриев нитрит",
    "e951": "Аспартам",
    "high fructose corn syrup": "Глюкозо-фруктозен сироп",
    "hfcs": "Глюкозо-фруктозен сироп",
    "artificial flavor": "Изкуствени аромати",
    "artificial colour": "Изкуствени оцветители",
    "artificial color": "Изкуствени оцветители",
    "e102": "Тартразин",
    "e110": "Жълто оцветител",
    "e124": "Понсо 4R"
}

# --------------------------------------------------
# Зареждане на EasyOCR
# --------------------------------------------------
@st.cache_resource

def load_reader():
    return easyocr.Reader(['bg', 'en'])

reader = load_reader()

# --------------------------------------------------
# Функция за OCR
# --------------------------------------------------
def extract_text(image):
    img_array = np.array(image)

    # OCR
    results = reader.readtext(img_array)

    extracted_text = "\n".join([res[1] for res in results])

    return extracted_text

# --------------------------------------------------
# Проверка за вредни съставки
# --------------------------------------------------
def find_harmful_ingredients(text):
    found = []

    normalized_text = text.lower()

    for keyword, description in HARMFUL_INGREDIENTS.items():
        if re.search(rf"\b{re.escape(keyword)}\b", normalized_text):
            found.append(description)

    return list(set(found))

# --------------------------------------------------
# Качване на снимка
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "📁 Качи снимка",
    type=["jpg", "jpeg", "png"]
)

# --------------------------------------------------
# Снимка от камера
# --------------------------------------------------
camera_image = st.camera_input("📷 Направи снимка")

image = None

if uploaded_file:
    image = Image.open(uploaded_file)

elif camera_image:
    image = Image.open(camera_image)

# --------------------------------------------------
# Обработка
# --------------------------------------------------
if image:
    st.image(image, caption="Избрано изображение", use_container_width=True)

    with st.spinner("Разпознаване на текст..."):
        text = extract_text(image)

    st.subheader("📄 Разпознат текст")

    if text.strip():
        st.text_area("OCR резултат", text, height=250)

        harmful = find_harmful_ingredients(text)

        st.subheader("⚠️ Открити вредни съставки")

        if harmful:
            for item in harmful:
                st.error(item)
        else:
            st.success("Не са открити вредни съставки.")

    else:
        st.warning("Не беше разпознат текст.")
```

---

# requirements.txt

```txt
streamlit
easyocr
opencv-python-headless
numpy
pillow
torch
torchvision
```

---

# Стартиране

## 1. Инсталация

```bash
pip install -r requirements.txt
```

## 2. Стартиране на приложението

```bash
streamlit run app.py
```

---

# Какво прави приложението

✅ Качване на снимка

✅ Заснемане от камера

✅ OCR разпознаване с EasyOCR

✅ Поддръжка на български и английски език

✅ Откриване на вредни съставки

✅ Показване на резултатите в реално време

---

# Идеи за подобрение

* Добавяне на база данни с повече съставки
* Оценка на риска (ниска / средна / висока)
* История на сканиранията
* Експорт в PDF
* Цветово маркиране върху самото изображение
* AI анализ на хранителния етикет
