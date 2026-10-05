from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# 1. CẤU HÌNH ĐÚNG ĐƯỜNG DẪN THƯ MỤC GỐC
# ==========================================
# Sử dụng 'r' đằng trước để Python hiểu đúng đường dẫn chứa dấu gạch chéo
root_dir = r"D:\SIC-AI\tài liệu đồ án"  # Thay đổi nếu thư mục chứa các chuyên ngành nằm ở chỗ khác
all_splits = []

# Cài đặt thuật toán chia nhỏ văn bản (Chunking) tối ưu cho tài liệu y khoa
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,   # Kích thước mỗi đoạn văn bản khoảng 600 ký tự
    chunk_overlap=80  # Độ chồng lấp để bảo toàn ngữ cảnh y khoa giữa các phần
)

# Quét tất cả các file PDF nằm trong thư mục gốc và mọi thư mục con (bệnh nội tiết, hô hấp, tim)
pdf_paths = list(Path(root_dir).rglob("*.pdf"))
print(f"🔍 Tìm thấy tổng cộng {len(pdf_paths)} file PDF phác đồ trong các chuyên ngành.")

for file_path in pdf_paths:
    try:
        # Sử dụng PyPDFLoader để đọc toàn bộ trang của từng file PDF
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()
        
        # Cắt nhỏ tài liệu thành các chunks
        splits = text_splitter.split_documents(documents)
        
        # Trích xuất tên chuyên ngành từ tên thư mục chứa file để làm Metadata
        ten_chuyen_nganh = file_path.parent.name
        
        # Gắn metadata cho từng chunk để hệ thống RAG phân biệt rõ ngữ cảnh chuyên khoa
        for split in splits:
            split.metadata["chuyen_nganh"] = ten_chuyen_nganh
            split.metadata["ten_file"] = file_path.name

        all_splits.extend(splits)
        print(f"✔ Đã xử lý chuyên ngành [{ten_chuyen_nganh}] - File: {file_path.name} ({len(splits)} chunks)")

    except Exception as e:
        print(f"❌ Lỗi khi đọc file {file_path}: {e}")

print(f"\n=> Tổng số lượng chunks tích lũy từ toàn bộ các chuyên ngành: {len(all_splits)}")

# ==========================================
# 2. TÍCH HỢP MÔ HÌNH EMBEDDING (SENTENCE-TRANSFORMERS)
# ==========================================
print("\nĐang tải mô hình embedding sentence-transformers...")
# Sử dụng mô hình mã nguồn mở chạy local, hoàn toàn miễn phí và bảo mật dữ liệu y tế
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
print("Đã tải xong mô hình Embedding thành công! ")
from langchain_community.vectorstores import Chroma

# ==========================================
# 3. CẤU HÌNH VÀ LƯU TRỮ VÀO CHROMADB (LOCAL)
# ==========================================
print("\nĐang khởi tạo và lưu trữ vector vào ChromaDB...")

# Lưu toàn bộ các chunks đã được nhúng vector vào Vector Database ChromaDB chạy local
vectorstore = Chroma.from_documents(
    documents=all_splits,         # Danh sách các đoạn văn bản kèm metadata (chuyên ngành, tên file)
    embedding=embedding_model,    # Mô hình embedding đã tải ở bước trước
    persist_directory="./chroma_db" # Thư mục lưu trữ cơ sở dữ liệu trên ổ cứng
)

print("🎉 Lưu trữ thành công vào ChromaDB tại thư mục './chroma_db'!")

# ==========================================
# 4. TEST THỬ CƠ CHẾ TRUY XUẤT (RETRIEVAL TEST)
# ==========================================
print("\n--- ĐANG KIỂM THỬ CƠ CHẾ TRUY XUẤT (RETRIEVAL) ---")

# Tạo bộ truy xuất (Retriever) từ ChromaDB, yêu cầu lấy ra 3 đoạn văn bản liên quan nhất
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# Thử đặt câu hỏi/triệu chứng giả lập của bác sĩ để kiểm tra kết quả tìm kiếm
test_query = "Triệu chứng và phác đồ điều trị bệnh tăng huyết áp hoặc đái tháo đường"
print(gr:=f"🔍 Câu hỏi test: '{test_query}'\n")

# Thực hiện truy xuất
relevant_docs = retriever.invoke(test_query)

# Hiển thị kết quả các đoạn văn bản tìm được
for i, doc in enumerate(relevant_docs, 1):
    print(f"--- KẾT QUẢ TRUY XUẤT {i} ---")
    print(f"Chuyên ngành: {doc.metadata.get('chuyen_nganh')}")
    print(f"Nguồn file: {doc.metadata.get('ten_file')}")
    print(f"Nội dung: {doc.page_content[:300]}...\n") # Hiển thị 300 ký tự đầu tiên của đoạn