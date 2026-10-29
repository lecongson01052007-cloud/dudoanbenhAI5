from __future__ import annotations

import os
import html
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
API = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
st.set_page_config(page_title="SIC • Trợ lý lâm sàng", page_icon="✚", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--ink:#172a31;--muted:#6b7e83;--teal:#176e69;--mint:#eaf5f1;--line:#e2eae7;--paper:#f7faf8}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--ink)}
.stApp{background:var(--paper)} h1,h2,h3{font-family:'Manrope',sans-serif;letter-spacing:-.035em}
[data-testid="stSidebar"]{background:#f0f6f3;border-right:1px solid var(--line)}
[data-testid="stSidebar"] h1{font-size:21px}.eyebrow{color:var(--teal);font-weight:700;font-size:12px;letter-spacing:.12em;text-transform:uppercase}
.hero{padding:26px 30px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(125deg,#fff 0%,#edf7f3 100%);margin:6px 0 22px}
.hero h1{margin:7px 0;font-size:35px}.hero p{color:var(--muted);margin:0;max-width:740px}
.panel{background:white;border:1px solid var(--line);border-radius:15px;padding:20px 22px;margin:12px 0}
.small-muted{color:var(--muted);font-size:13px}.chip{display:inline-block;border-radius:999px;background:var(--mint);color:var(--teal);padding:5px 11px;font-size:12px;font-weight:600}
div.stButton>button[kind="primary"]{background:var(--teal);border:0;border-radius:10px;font-weight:650;min-height:44px}
div[data-testid="stMetric"]{background:white;padding:14px 17px;border:1px solid var(--line);border-radius:14px}
</style>
""", unsafe_allow_html=True)


def api_get(path: str):
    return requests.get(API + path, timeout=20)


def api_post(path: str, **kwargs):
    return requests.post(API + path, timeout=180, **kwargs)


def header(tag: str, title: str, desc: str):
    st.markdown(f'<div class="hero"><div class="eyebrow">{tag}</div><h1>{title}</h1><p>{desc}</p></div>', unsafe_allow_html=True)


def citation_card(source: dict):
    citation_id, disease = html.escape(str(source.get("citation_id", "Nguồn"))), html.escape(str(source.get("disease", "")))
    section, path = html.escape(str(source.get("section", ""))), html.escape(str(source.get("source", "")))
    specialty, score = html.escape(str(source.get("specialty", ""))), html.escape(str(source.get("score", "")))
    st.markdown(f"**[{citation_id}] {disease} · {section}**  \n<span class='small-muted'>{path} · {specialty} · độ phù hợp {score}</span>", unsafe_allow_html=True)
    with st.expander("Xem đoạn trích nguồn"):
        st.write(source.get("text", ""))


with st.sidebar:
    st.markdown("### ✚ SIC Clinical")
    st.caption("Hệ thống hỗ trợ bác sĩ · RAG + Gemini")
    page = st.radio("Không gian làm việc", ["Phân tích ca bệnh", "Tra cứu kho tri thức", "Quản lý tài liệu"], label_visibility="collapsed")
    st.divider()
    try:
        health = api_get("/health").json()
        docs = api_get("/documents").json()
        st.markdown("**Trạng thái hệ thống**")
        st.caption("● API đang hoạt động" if health.get("status") == "ok" else "API không khả dụng")
        if not health.get("llm_configured"):
            st.warning("Chưa cấu hình GOOGLE_API_KEY; tra cứu RAG hoạt động, phân tích Gemini cần thêm khóa vào tệp .env.")
        st.caption(f"{docs.get('total_files', 0)} tài liệu · {docs.get('total_chunks', 0)} đoạn")
    except requests.RequestException:
        st.error("Chưa kết nối được backend.")
    st.divider()
    st.caption("Bản thử nghiệm hỗ trợ bác sĩ. Mọi nhận định cần được kiểm tra với hồ sơ và tài liệu nguồn.")


if page == "Phân tích ca bệnh":
    header("PHÂN TÍCH LÂM SÀNG", "Xem xét ca bệnh", "Nhập thông tin ca bệnh có cấu trúc để nhận gợi ý chẩn đoán sơ bộ kèm đoạn nguồn truy xuất.")
    with st.form("case_form"):
        st.markdown("#### Thông tin người bệnh")
        a, b, c = st.columns([1, 1, 2])
        age = a.number_input("Tuổi", min_value=0, max_value=120, value=45)
        sex = b.selectbox("Giới", ["Nam", "Nữ", "Khác"])
        specialty = c.selectbox("Chuyên khoa", ["Tự động", "Nội tiết", "Hô hấp", "Tim mạch"])
        st.markdown("#### Triệu chứng")
        d, e = st.columns([2, 1])
        main = d.text_input("Triệu chứng chính", placeholder="Ví dụ: khó thở tăng dần khi gắng sức")
        duration = e.text_input("Thời gian diễn tiến", placeholder="Ví dụ: 3 ngày")
        associated = st.text_input("Triệu chứng kèm theo", placeholder="Phân cách bằng dấu phẩy")
        history = st.text_area("Tiền sử liên quan", placeholder="Bệnh nền, thuốc đang dùng, dị ứng, tiền sử gia đình…", height=92)
        st.markdown("#### Xét nghiệm")
        lab_count = st.number_input("Số kết quả xét nghiệm", 0, 20, 0, key="lab_count")
        labs = []
        for i in range(int(lab_count)):
            x, y, z = st.columns([2, 1, 1])
            name = x.text_input("Tên xét nghiệm", key=f"lab_name_{i}", placeholder="Ví dụ: HbA1c")
            value = y.text_input("Giá trị", key=f"lab_value_{i}")
            unit = z.text_input("Đơn vị", key=f"lab_unit_{i}", placeholder="%")
            if name and value:
                labs.append({"name": name, "value": value, "unit": unit})
        submitted = st.form_submit_button("✦  Phân tích ca bệnh", type="primary", use_container_width=True)
    if submitted:
        if not main.strip() or not duration.strip():
            st.warning("Vui lòng nhập triệu chứng chính và thời gian diễn tiến.")
        else:
            payload = {"age": age, "sex": sex, "specialty": specialty, "main_symptom": main, "duration": duration, "associated_symptoms": [x.strip() for x in associated.split(",") if x.strip()], "history": history, "labs": labs}
            with st.spinner("Đang truy xuất hướng dẫn và chuẩn bị báo cáo… lần đầu có thể cần tải mô hình embedding"):
                try:
                    response = api_post("/analyze", json=payload)
                    if response.status_code != 200:
                        st.error(response.json().get("detail", "Không thể phân tích ca."))
                    else:
                        data = response.json(); answer = data["answer"]
                        st.session_state["last_analysis"] = {"case": payload, "data": data, "at": datetime.now().isoformat(timespec="minutes")}
                except requests.RequestException as exc:
                    st.error(f"Không gọi được backend: {exc}")
    analysis = st.session_state.get("last_analysis")
    if analysis:
        answer, data = analysis["data"]["answer"], analysis["data"]
        st.divider()
        st.markdown("### Báo cáo gợi ý")
        urgency = answer.get("urgency", "routine")
        if urgency == "emergency": st.error("MỨC KHẨN: CẤP CỨU · " + answer.get("urgency_reason", ""))
        elif urgency == "urgent": st.warning("MỨC KHẨN: ƯU TIÊN ĐÁNH GIÁ · " + answer.get("urgency_reason", ""))
        else: st.info("MỨC KHẨN: THƯỜNG QUY · " + answer.get("urgency_reason", ""))
        st.markdown(f"<div class='panel'><div class='eyebrow'>NHẬN ĐỊNH SƠ BỘ · {data.get('specialty','')}</div><p>{answer.get('impression','')}</p></div>", unsafe_allow_html=True)
        st.markdown("#### Chẩn đoán phân biệt")
        for i, item in enumerate(answer.get("differential", []), 1):
            st.markdown(f"**{i}. {item.get('diagnosis','')}**  \n{item.get('rationale','')}  \n*Nguồn: {', '.join(item.get('citations', [])) or 'Chưa gắn trích dẫn'}*")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Thông tin cần bổ sung")
            for item in answer.get("missing_information", []): st.markdown(f"- {item}")
        with col2:
            st.markdown("#### Đánh giá có thể cân nhắc")
            for item in answer.get("suggested_evaluation", []): st.markdown(f"- {item}")
        if answer.get("limitations"): st.caption("Giới hạn: " + answer["limitations"])
        if data.get("sources"):
            st.markdown("#### Đoạn nguồn đã truy xuất")
            for source in data["sources"]: citation_card(source)
        st.divider()
        st.markdown("**Bác sĩ xác nhận / hiệu chỉnh**")
        st.text_area("Ghi chú chuyên môn", key="doctor_note", placeholder="Ghi nhận hiệu chỉnh hoặc kết luận sau khi đối chiếu hồ sơ…")
        if st.button("Lưu xác nhận của bác sĩ", type="primary"):
            note = st.session_state.get("doctor_note", "").strip()
            if not note:
                st.warning("Nhập ghi chú xác nhận hoặc hiệu chỉnh trước khi lưu.")
            else:
                try:
                    res = api_post("/feedback", json={"note": note, "timestamp": datetime.now().isoformat(timespec="minutes")})
                    st.success("Đã lưu ghi chú hiệu chỉnh. Hệ thống chỉ lưu ghi chú và thời gian, không lưu thông tin ca bệnh.") if res.ok else st.error("Không lưu được ghi chú.")
                except requests.RequestException as exc: st.error(f"Không gọi được backend: {exc}")
        st.caption("Ghi chú được lưu cục bộ tại data/clinician_feedback.jsonl. Không nhập thông tin nhận dạng người bệnh.")

elif page == "Tra cứu kho tri thức":
    header("KHO TRI THỨC", "Tra cứu hướng dẫn", "Tìm kiếm trực tiếp trên các đoạn tài liệu chuyên môn và mở trích đoạn gốc để kiểm tra.")
    with st.form("search_form"):
        query = st.text_input("Câu hỏi hoặc triệu chứng", placeholder="Ví dụ: tiêu chuẩn chẩn đoán đái tháo đường type 2")
        c1, c2 = st.columns([2, 1])
        specialty = c1.selectbox("Chuyên khoa", ["Tất cả", "Nội tiết", "Hô hấp", "Tim mạch"])
        top_k = c2.select_slider("Số kết quả", options=[3, 5, 8], value=5)
        submitted = st.form_submit_button("Tìm trong kho tri thức", type="primary")
    if submitted and query.strip():
        with st.spinner("Đang tìm kiếm ngữ nghĩa…"):
            try:
                response = api_post("/search", json={"query": query, "specialty": specialty, "top_k": top_k})
                if response.ok:
                    results = response.json()["results"]
                    st.markdown(f"### {len(results)} đoạn phù hợp")
                    for item in results: citation_card(item); st.divider()
                else: st.error(response.json().get("detail", "Tìm kiếm thất bại."))
            except requests.RequestException as exc: st.error(f"Không gọi được backend: {exc}")

else:
    header("QUẢN LÝ KHO", "Tài liệu chuyên môn", "Theo dõi phạm vi kho tri thức, nạp Markdown mới và lập chỉ mục lại cho bộ tìm kiếm.")
    try:
        data = api_get("/documents").json()
        a,b,c = st.columns(3)
        a.metric("Tài liệu", data["total_files"]); b.metric("Đoạn nội dung", data["total_chunks"]); c.metric("Chuyên khoa có tài liệu", sum(1 for n in data["specialties"].values() if n))
        st.markdown("#### Phạm vi theo chuyên khoa")
        st.dataframe(pd.DataFrame([{"Chuyên khoa": k, "Số tài liệu": v, "Trạng thái": "Có dữ liệu" if v else "Chưa có tài liệu nguồn"} for k,v in data["specialties"].items()]), hide_index=True, use_container_width=True)
        st.markdown("#### Danh mục nguồn")
        st.dataframe(pd.DataFrame(data["documents"]), hide_index=True, use_container_width=True)
        st.markdown("#### Nạp tài liệu Markdown")
        upload = st.file_uploader("Chọn tệp .md", type=["md"], accept_multiple_files=False)
        x,y = st.columns(2)
        if x.button("Nạp tệp và cập nhật chỉ mục", type="primary", disabled=upload is None):
            with st.spinner("Đang nạp kho và lập chỉ mục embeddings…"):
                res = api_post("/ingest", files={"file": (upload.name, upload.getvalue(), "text/markdown")})
                st.success(f"Đã lập chỉ mục {res.json().get('indexed_chunks',0)} đoạn.") if res.ok else st.error(res.json().get("detail", "Nạp thất bại."))
        if y.button("Lập chỉ mục lại toàn bộ Markdown"):
            with st.spinner("Đang lập chỉ mục lại toàn bộ kho…"):
                res = api_post("/ingest")
                st.success(f"Đã lập chỉ mục {res.json().get('indexed_chunks',0)} đoạn.") if res.ok else st.error(res.json().get("detail", "Nạp thất bại."))
        st.info("PDF ghi tài liệu Tim mạch đang chờ; workspace hiện có 25 tệp Markdown trong thư mục phác đồ bệnh tim và chúng được lập chỉ mục. Xác minh nguồn và rà soát chuyên môn trước khi dùng. Tệp nạp phải là Markdown và cần được bác sĩ rà soát.")
    except requests.RequestException as exc: st.error(f"Không lấy được danh mục: {exc}")
