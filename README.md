# dudoanbenhAI5
# Giao diện trang web
  👤 1. Nhóm Trang dành cho Bệnh nhân (Patient Portal)
Nhóm trang này giúp người dùng cuối tự kiểm tra sức khỏe cá nhân và quản lý hồ sơ của mình.

Trang 1: Trang chủ / Tổng quan sức khỏe (Dashboard)

Tính năng: Hiển thị biểu đồ lịch sử đo huyết áp, nhịp tim, cholesterol gần đây; cảnh báo mức độ rủi ro tim mạch mới nhất (Thấp / Trung bình / Cao).

Trang 2: Khảo sát rủi ro nhanh (Quick Assessment / AI Prediction)

Tính năng: Form nhập liệu đơn giản (Tuổi, giới tính, huyết áp, nhịp tim, tiểu sử hút thuốc, v.v.). Bấm nút để hệ thống chạy mô hình ML dự đoán tỷ lệ nguy cơ mắc bệnh tim kèm theo lời khuyên thay đổi lối sống.

Trang 3: Hồ sơ y tế cá nhân (Medical History & Profile)

Tính năng: Nơi lưu trữ toàn bộ kết quả xét nghiệm, lịch sử khám bệnh, file điện tâm đồ (ECG) đã tải lên trước đó để có thể xem lại bất cứ lúc nào.

🩺 2. Nhóm Trang dành cho Bác sĩ & Chuyên gia (Doctor Portal - Trọng tâm RAG)
Đây là màn hình làm việc chính của bác sĩ để hỗ trợ chẩn đoán nhanh và chính xác dựa trên sự hỗ trợ của AI.

Trang 4: Danh sách bệnh nhân & Hàng chờ khám (Patient Queue)

Tính năng: Bảng danh sách các bệnh nhân được gán cho bác sĩ đó. Có bộ lọc tìm kiếm theo tên, mức độ khẩn cấp (ca nào nguy cơ cao được gắn nhãn đỏ ưu tiên hiển thị lên đầu).

Trang 5: Giao diện Phân tích ca bệnh thông minh (AI Clinical Decision Support)

Tính năng cốt lõi (Màn hình làm việc chính của RAG):

Cột nhập liệu: Điền triệu chứng lâm sàng chi tiết và kết quả xét nghiệm chuyên sâu (Troponin, Cholesterol, Đường huyết, v.v.).

Khu vực kết quả AI: Hiển thị báo cáo nhận định sơ bộ, chẩn đoán phân biệt, và đặc biệt có phần Trích dẫn nguồn y văn (RAG Citations) để bác sĩ bấm vào xem đoạn sách/phác đồ gốc.

Nút xác nhận: Cho phép bác sĩ duyệt, chỉnh sửa hoặc ghi đè kết quả của AI để lưu vào bệnh án chính thức.

Trang 6: Tra cứu kho tri thức y khoa (Medical Knowledge Base Search)

Tính năng: Thanh tìm kiếm trực tiếp vào Vector Database (giống như một "Google thu nhỏ" nội bộ của bệnh viện), cho phép bác sĩ tra cứu nhanh các hướng dẫn điều trị bệnh tim mới nhất của AHA/ACC hoặc Bộ Y tế.

⚙️ 3. Nhóm Trang dành cho Quản trị viên hệ thống (Admin & Research Portal)
Dành cho người quản lý hệ thống Cloud hoặc nhà nghiên cứu y học dữ liệu.

Trang 7: Quản lý người dùng & Phân quyền (User Management)

Tính năng: Thêm/sửa/xóa tài khoản, phân quyền rõ ràng ai là Bệnh nhân, ai là Bác sĩ, ai là Quản trị viên (đảm bảo tính bảo mật đa người dùng - multi-tenant).

Trang 8: Giám sát hệ thống Cloud & Hiệu suất AI (System & AI Monitoring)

Tính năng: Theo dõi lượng truy cập đồng thời (API traffic), tốc độ phản hồi của mô hình LLM/RAG, trạng thái hoạt động của cơ sở dữ liệu đám mây.

# train model
  HƯỚNG DẪN TỪ A-Z: XÂY DỰNG TRỢ LÝ ẢO CHẨN ĐOÁN TIM MẠCH (RAG + LLM)

Dành cho người mới bắt đầu tiếp cận công nghệ Trí tuệ nhân tạo và Y tế số

PHẦN 1: TỔNG QUAN - HỆ THỐNG NÀY LÀ GÌ VÀ HOẠT ĐỘNG RA SAO?

Hãy tưởng tượng bạn đang xây dựng một "Cố vấn Y khoa thông minh".

Vấn đề thông thường: Khi hỏi các mô hình AI thông thường (như ChatGPT bản miễn phí) về y tế, chúng có thể bịa ra thông tin (gọi là ảo giác), rất nguy hiểm trong ngành y.

Giải pháp RAG (Retrieval-Augmented Generation): Giống như một học sinh đi thi được mang theo sách giáo khoa vào phòng thi. Trước khi AI trả lời bác sĩ, nó sẽ chạy đi tìm các tài liệu chuẩn (sách hướng dẫn của Bộ Y tế, cẩm nang tim mạch AHA/ESC), sau đó đọc tài liệu đó rồi mới trả lời. Nhờ vậy, câu trả lời luôn có căn cứ chính xác.

PHẦN 2: CHUẨN BỊ MÔI TRƯỜNG VÀ CÔNG CỤ (DÀNH CHO NGƯỜI MỚI)

Trước khi viết code, bạn cần chuẩn bị các công cụ sau trên máy tính:

Python (Phiên bản 3.10 trở lên): Ngôn ngữ lập trình chính.

Trình soạn thảo code: Visual Studio Code (VS Code) là lựa chọn tốt nhất.

API Key: Khóa truy cập OpenAI (để dùng mô hình LLM và Embedding).

Các thư viện Python cần cài đặt (requirements.txt)

Tạo một file tên là requirements.txt với nội dung:

fastapi==0.110.0
uvicorn==0.28.0
streamlit==1.32.0
langchain==0.1.16
langchain-community==0.0.32
langchain-openai==0.1.3
chromadb==0.4.24
pypdf==4.1.0
python-dotenv==1.0.1


PHẦN 3: CẤU TRÚC THƯ MỤC DỰ ÁN (BẠN CẦN TẠO CÁC FILE NÀO?)

Hãy tạo một thư mục tên là cardio-assistant và sắp xếp các file bên trong như sau:

cardio-assistant/
│
├── data/
│   ├── raw_guidelines/      📍 (1) Nơi chứa các file PDF tài liệu y khoa của bạn
│   └── vector_db/           📍 (2) Thư mục hệ thống tự sinh ra để lưu "trí nhớ" của AI
│
├── src/
│   ├── __init__.py          📍 (3) File đánh dấu thư mục là package Python
│   ├── config.py            📍 (4) File lưu cấu hình, mật khẩu API
│   ├── ingest.py            📍 (5) File "đọc sách" và nạp dữ liệu vào trí nhớ AI
│   ├── rag_engine.py        📍 (6) "Bộ não" xử lý tìm kiếm tài liệu và gọi AI
│   ├── api.py               📍 (7) Cổng giao tiếp trung gian (Backend)
│   └── app.py               📍 (8) Giao diện màn hình cho bác sĩ dùng (Frontend)
│
├── requirements.txt         📍 (9) Danh sách thư viện cần cài
└── .env                     📍 (10) File chứa khóa bí mật (API Key)


PHẦN 4: HƯỚNG DẪN CHI TIẾT TỪNG BƯỚC LÀM TỪNG FILE

Bước 1: Tạo file cấu hình và bảo mật

File .env (Đặt ở thư mục gốc để chứa khóa bí mật, không chia sẻ file này lên mạng):

OPENAI_API_KEY=sk-proj-dien-khoa-api-cua-ban-vao-day


File src/config.py (Đọc cấu hình từ hệ thống):

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_DB_DIR = "./data/vector_db"
RAW_DATA_DIR = "./data/raw_guidelines"
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
LLM_MODEL_NAME = "gpt-4o"


Bước 2: Xây dựng "Bộ nhớ" cho AI (Nạp tài liệu y khoa)

Bạn hãy copy các file PDF hướng dẫn chẩn đoán bệnh tim mạch vào thư mục data/raw_guidelines/. Sau đó viết file src/ingest.py để AI đọc sách và ghi nhớ:

File src/ingest.py:

import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.config import RAW_DATA_DIR, VECTOR_DB_DIR, EMBEDDING_MODEL_NAME

def build_vector_database():
    print("Step 1: Đang quét thư mục chứa tài liệu y khoa...")
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)
        print(f"Hãy bỏ các file PDF vào thư mục {RAW_DATA_DIR} rồi chạy lại script này!")
        return

    loader = PyPDFDirectoryLoader(RAW_DATA_DIR)
    docs = loader.load()
    
    if len(docs) == 0:
        print("Không tìm thấy file PDF nào! Vui lòng thêm tài liệu vào thư mục raw_guidelines.")
        return

    print(f"Step 2: Đã tải {len(docs)} trang tài liệu. Đang cắt nhỏ văn bản...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    splits = text_splitter.split_documents(docs)

    print("Step 3: Đang chuyển đổi văn bản thành Vector và lưu vào Vector Database...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
    
    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )
    print("HOÀN TẤT! Trí nhớ y khoa đã được thiết lập thành công.")

if __name__ == "__main__":
    build_vector_database()


Bước 3: Xây dựng Bộ não RAG (Xử lý câu hỏi và tra cứu)

File này sẽ nhận triệu chứng bệnh nhân, tìm kiếm trong kho sách, rồi ghép vào câu lệnh (Prompt) gửi cho ChatGPT.

File src/rag_engine.py:

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from src.config import VECTOR_DB_DIR, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME

class CardioRAGAnalyzer:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
        self.vectorstore = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        self.llm = ChatOpenAI(model=LLM_MODEL_NAME, temperature=0.1)
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", 
             "Bạn là trợ lý y khoa AI hỗ trợ bác sĩ. Hãy phân tích triệu chứng dựa DUY NHẤT trên các tài liệu y khoa dưới đây. "
             "Tuyệt đối không bịa đặt thông tin ngoài tài liệu.\n\n"
             "--- TÀI LIỆU Y KHOA THAM KHẢO ---\n{context}"),
            ("human", 
             "Thông tin bệnh nhân:\n- Triệu chứng: {symptoms}\n- Xét nghiệm: {lab_results}\n\n"
             "Hãy đưa ra báo cáo gồm: 1. Mức độ rủi ro, 2. Chẩn đoán phân biệt, 3. Đề xuất xét nghiệm, 4. Nguồn trích dẫn.")
        ])

    def analyze(self, symptoms: str, lab_results: str):
        docs = self.retriever.invoke(f"{symptoms} {lab_results}")
        context = "\n\n".join([d.page_content for d in docs])
        sources = list(set([d.metadata.get("source", "Tài liệu y khoa") for d in docs]))

        chain = self.prompt_template | self.llm
        response = chain.invoke({"context": context, "symptoms": symptoms, "lab_results": lab_results})

        return {"analysis_report": response.content, "sources": sources}


Bước 4: Tạo Cổng Giao Tiếp Backend (FastAPI)

Giúp hệ thống đóng vai trò như một máy chủ nhận dữ liệu từ giao diện người dùng.

File src/api.py:

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.rag_engine import CardioRAGAnalyzer

app = FastAPI(title="Cardio RAG API")
analyzer = CardioRAGAnalyzer()

class PatientData(BaseModel):
    symptoms: str
    lab_results: str

@app.post("/api/v1/analyze")
def analyze_case(data: PatientData):
    try:
        result = analyzer.analyze(data.symptoms, data.lab_results)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


Bước 5: Tạo Giao Diện Cho Bác Sĩ (Streamlit Frontend)

Tạo trang web trực quan để bác sĩ thao tác dễ dàng mà không cần biết lập trình.

File src/app.py:

import streamlit as st
import requests

st.set_page_config(page_title="Trợ lý Chẩn đoán Tim mạch", layout="wide")
st.title("🫀 Trợ lý Ảo Hỗ trợ Sơ bộ Chẩn đoán Tim Mạch (RAG + AI)")

with st.form("form"):
    col1, col2 = st.columns(2)
    with col1:
        symptoms = st.text_area("Triệu chứng lâm sàng (Ví dụ: Đau tức ngực, khó thở...)")
    with col2:
        lab_results = st.text_area("Kết quả xét nghiệm (Ví dụ: Cholesterol cao, Troponin bình thường...)")
    submit = st.form_submit_button("Phân tích ca bệnh")

if submit:
    if not symptoms or not lab_results:
        st.warning("Vui lòng điền đầy đủ thông tin!")
    else:
        with st.spinner("AI đang tra cứu phác đồ và phân tích..."):
            try:
                res = requests.post("http://localhost:8000/api/v1/analyze", json={"symptoms": symptoms, "lab_results": lab_results})
                if res.status_code == 200:
                    data = res.json()["data"]
                    st.success("Phân tích thành công!")
                    st.markdown("### 📋 Báo cáo chẩn đoán sơ bộ")
                    st.markdown(data["analysis_report"])
                    st.markdown("### 📚 Tài liệu tham khảo")
                    for src in data["sources"]:
                        st.text(f"- {src}")
                else:
                    st.error("Lỗi kết nối Backend.")
            except Exception as e:
                st.error(f"Lỗi: {e}")


PHẦN 5: CÁCH CHẠY THỬ HỆ THỐNG TRÊN MÁY TÍNH CỦA BẠN

Cài đặt thư viện: Mở terminal tại thư mục dự án và chạy lệnh:

pip install -r requirements.txt


Nạp dữ liệu: Đặt 1 file PDF y khoa về tim mạch vào data/raw_guidelines/, sau đó chạy:

python -m src.ingest


Khởi động Backend API:

uvicorn src.api:app --reload --port 8000


Khởi động Giao diện Web (Mở một cửa sổ Terminal khác):

streamlit run src.app.py


Bây giờ bạn truy cập trình duyệt theo đường dẫn hiển thị (thường là http://localhost:8501) để bắt đầu trải nghiệm hệ thống trợ lý ảo của riêng mình!
Trang 9: Quản lý tài liệu tri thức RAG (Knowledge Management)

Tính năng: Nơi Admin upload các file PDF tài liệu y khoa mới hoặc cập nhật phác đồ điều trị để hệ thống tự động băm nhỏ và cập nhật vào Vector Database.
