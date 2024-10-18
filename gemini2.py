import streamlit as st
import google.generativeai as genai
import PyPDF2
import os

# Gemini 모델 설정 함수
def setup_gemini_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

# PDF 파일 읽기 함수
def read_pdf(file_path):
    if not os.path.exists(file_path):
        return "파일을 찾을 수 없습니다."
    
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def main():
    st.title("AI Research Paper Review Team")

    st.header("Team Structure")
    st.markdown("""
    1. **Sam (AI PhD)**: Explains paper content in simple terms
    2. **Jenny (AI & Education PhD)**: Simplifies and expands on Sam's draft
    3. **Will (Team Leader)**: Finalizes the report
    """)

    st.header("Workflow")
    st.markdown("""
    1. Sam's Initial Analysis
    2. Jenny's Review and Enhancement
    3. Will's Final Review and Compilation
    """)

    user_input = st.text_area("Enter the AI research paper here:")
    if st.button("Process Paper"):
        if user_input:
            with st.spinner("Processing..."):
                response = process_user_input(user_input)
                st.subheader("Final Report")
                st.write(response)
        else:
            st.warning("Please enter a research paper to process.")

def process_user_input(user_input):
    # Sam의 초기 분석
    sam_prompt = f"""
    You are Sam, an AI PhD graduate. Analyze the following AI research paper:
    {user_input}
    Provide an initial draft explaining the key points, methodologies, and findings in simpler terms.
    """
    sam_response = model.generate_content(sam_prompt).text

    # Jenny의 리뷰 및 개선
    jenny_prompt = f"""
    You are Jenny, with PhDs in AI and Education. Review and enhance the following draft:
    {sam_response}
    Simplify the language further, add educational context, and expand on areas needing more explanation.
    """
    jenny_response = model.generate_content(jenny_prompt).text

    # Will의 최종 검토 및 편집
    will_prompt = f"""
    You are Will, the team leader. Review and finalize the following report:
    {jenny_response}
    Ensure all key points are covered, verify accuracy, maintain consistency, and structure the report as follows:
    1. Executive Summary
    2. Introduction to the Research Topic
    3. Key Findings and Methodologies
    4. Simplified Explanation of Complex Concepts
    5. Real-world Applications and Implications
    6. Conclusion and Future Research Directions
    """
    final_report = model.generate_content(will_prompt).text

    return final_report

if __name__ == "__main__":
    main()

# API 키 입력
api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")

if api_key:
    try:
        model = setup_gemini_model(api_key)
        st.success("API 키가 성공적으로 설정되었습니다.")

        # PDF 파일 경로 입력
        pdf_path = st.text_input("PDF 파일 경로를 입력하세요:", value=r"C:\Users\eraje\projects\cuoserAI\sangje.pdf")

        if pdf_path:
            # 경로의 백슬래시를 정규화
            pdf_path = os.path.normpath(pdf_path)
            
            # PDF 내용 읽기
            pdf_content = read_pdf(pdf_path)
            
            if pdf_content != "파일을 찾을 수 없습니다.":
                st.success("PDF 파일을 성공적으로 읽었습니다.")
                
                # 사용자 질문 입력
                user_question = st.text_input("PDF에 대해 질문하세요:")
                
                if user_question:
                    # Gemini API에 질문과 PDF 내용 전달
                    prompt = f"다음 PDF 내용에 대해 답변해주세요. 내용: {pdf_content}\n\n질문: {user_question}"
                    response = model.generate_content(prompt)
                    
                    # 응답 출력
                    st.write("AI의 응답:")
                    st.write(response.text)
            else:
                st.error(pdf_content)
    except Exception as e:
        st.error(f"API 키 설정 중 오류가 발생했습니다: {str(e)}")

# 스트림릿 앱 실행 방법 안내
st.sidebar.markdown("""
## 앱 실행 방법
1. Gemini API 키를 입력하세요.
2. PDF 파일의 경로를 입력하세요.
3. PDF에 대한 질문을 입력하세요.

터미널에서 다음 명령어로 앱을 실행하세요:
""")
