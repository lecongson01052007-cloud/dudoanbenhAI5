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
print("Đã tải xong mô hình Embedding thành công! Sẵn sàng bàn giao dữ liệu cho Thành viên 5 đưa vào ChromaDB.")
