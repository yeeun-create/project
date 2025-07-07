import streamlit as st
import openai
import io
import os
from PIL import Image
import requests
from dotenv import load_dotenv

# .env 파일에서 환경변수 불러오기 (없으면 무시)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("맞춤형 레시피 추천 생성기")

# 입력 폼
with st.form("recipe_form"):
    ingredients = st.text_input("보유 재료를 입력하세요 (쉼표로 구분)")
    goal = st.text_input("식단 목적을 입력하세요 (예: 다이어트, 고단백 등)")
    submitted = st.form_submit_button("레시피 추천 받기")

def get_recipe(ingredients, goal):
    prompt = f"""
    아래 조건에 맞는 오늘의 맞춤 레시피를 추천해줘.
    1. 사용 가능한 재료: {ingredients}
    2. 식단 목적: {goal}
    아래 형식으로 답변해줘.
    메뉴 이름:
    요리 과정:
    예상 칼로리:
    추천 이유:
    """
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content if hasattr(response.choices[0], "message") else response.choices[0].text

def get_recipe_card_image(recipe_text):
    # DALL·E API를 활용해 카드 이미지 생성 (텍스트 프롬프트 기반)
    dalle_prompt = f"레시피 카드 디자인, 한글, 내용: {recipe_text}"
    response = openai.images.generate(
        model="dall-e-3",
        prompt=dalle_prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    # 이미지 다운로드
    image_response = requests.get(image_url)
    img = Image.open(io.BytesIO(image_response.content))
    return img

if submitted and ingredients and goal:
    with st.spinner("GPT-4o가 레시피를 생성 중입니다..."):
        recipe = get_recipe(ingredients, goal)
    st.subheader("오늘의 맞춤 레시피")
    st.text(recipe)

    with st.spinner("레시피 카드 이미지를 생성 중입니다..."):
        img = get_recipe_card_image(recipe)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.image(img, caption="레시피 카드", use_column_width=True)
        st.download_button(
            label="레시피 카드 이미지 다운로드",
            data=byte_im,
            file_name="recipe_card.png",
            mime="image/png"
        )
