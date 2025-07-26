import streamlit as st

def QuydoiDiemvact(Diemdgnl: float, Uutiengiai=0, Uutienkv=0) -> float:
    return round(27 + ((Diemdgnl - 850) * 3 / 350) + Uutiengiai + Uutienkv, 2)

def QuydoiDiemhsa(Diemhsa: float, Uutien=0) -> float:
    return round(27 + ((Diemhsa - 100) * 3 / 50) + Uutien, 2)

def NoisuyTuyentinh(x, a, b, c, d):
    if x < a or x > b:
        raise ValueError("Điểm nằm ngoài khoảng nội suy.")
    return round(c + ((x - a) / (b - a)) * (d - c), 2)

# Khoảng quy đổi theo từng phương thức
KhoangQuydoiTheoPhuongThuc = {
    "V-ACT": [
        (28.51, 30.00, 28.0, 30.0),
        (28.14, 28.51, 27.3, 28.0),
        (27.86, 28.14, 26.75, 27.3),
        (27.51, 27.86, 26.0, 26.75),
        (27.16, 27.51, 25.25, 26.0),
        (27.00, 27.16, 24.0, 25.25),
    ],
    "HSA": [
        (28.2, 30.0, 28.0, 30.0),
        (27.38, 28.2, 27.3, 28.0),
        (26.78, 27.38, 26.75, 27.3),
        (26.0, 26.78, 26.0, 26.75),
        (25.2, 26.0, 25.25, 26.0),
        (24.0, 25.2, 24.0, 25.25),
    ],
    "THPT": [
        (28.0, 30.0, 28.0, 30.0),
        (27.3, 28.0, 27.3, 28.0),
        (26.75, 27.3, 26.75, 27.3),
        (26.0, 26.75, 26.0, 26.75),
        (25.25, 26.0, 25.25, 26.0),
        (24.0, 25.25, 24.0, 25.25),
    ]
}

def main():
    st.title("Công cụ quy đổi điểm xét tuyển FTU chương trình chuẩn")

    phuongthuc_display = st.selectbox("Chọn phương thức xét tuyển:", ["V-ACT", "HSA", "THPT Quốc gia (A00 hoặc tổ hợp khác)"])
    phuongthuc_key = "V-ACT" if "V-ACT" in phuongthuc_display else ("HSA" if "HSA" in phuongthuc_display else "THPT")

    if phuongthuc_key == "V-ACT":
        diem = st.number_input("Nhập điểm ĐGNL V-ACT (thang 1200):", min_value=0.0, max_value=1200.0)
        uutiengiai = st.number_input("Điểm ưu tiên do đạt giải:", min_value=0.0, value=0.0)
        uutienkv = st.number_input("Điểm ưu tiên KV/ĐT:", min_value=0.0, value=0.0)
        if st.button("Tính điểm"):
            diem30 = QuydoiDiemvact(diem, uutiengiai, uutienkv)
            st.write(f"Điểm quy đổi về thang 30: {diem30}")
            for (a, b, c, d) in KhoangQuydoiTheoPhuongThuc[phuongthuc_key]:
                if a <= diem30 <= b:
                    diemQuydoi = NoisuyTuyentinh(diem30, a, b, c, d)
                    st.write(f"Điểm tương đương nội suy theo tổ hợp A00: {diemQuydoi}")
                    break
            else:
                st.warning("Điểm nằm ngoài phạm vi nội suy.")

    elif phuongthuc_key == "HSA":
        diem = st.number_input("Nhập điểm HSA (thang 150):", min_value=0.0, max_value=150.0)
        uutien = st.number_input("Tổng điểm ưu tiên (nếu có):", min_value=0.0, value=0.0)
        if st.button("Tính điểm"):
            diem30 = QuydoiDiemhsa(diem, uutien)
            st.write(f"Điểm quy đổi về thang 30: {diem30}")
            for (a, b, c, d) in KhoangQuydoiTheoPhuongThuc[phuongthuc_key]:
                if a <= diem30 <= b:
                    diemQuydoi = NoisuyTuyentinh(diem30, a, b, c, d)
                    st.write(f"Điểm tương đương nội suy theo tổ hợp A00: {diemQuydoi}")
                    break
            else:
                st.warning("Điểm nằm ngoài phạm vi nội suy.")

    elif phuongthuc_key == "THPT":
        diem = st.number_input("Nhập điểm tổ hợp (thang 30):", min_value=0.0, max_value=30.0)
        tohop = st.text_input("Nhập mã tổ hợp (ví dụ: A00, D01, A01...):", value="A00")
        if st.button("Tính điểm"):
            diem30 = diem
            if tohop.upper() != "A00":
                diem30 -= 1.0
                st.write("Đã trừ 1.0 điểm để quy đổi về tổ hợp A00")
            st.write(f"Điểm sau điều chỉnh: {diem30}")
            for (a, b, c, d) in KhoangQuydoiTheoPhuongThuc[phuongthuc_key]:
                if a <= diem30 <= b:
                    diemQuydoi = NoisuyTuyentinh(diem30, a, b, c, d)
                    st.write(f"Điểm tương đương nội suy theo tổ hợp A00: {diemQuydoi}")
                    break
            else:
                st.warning("Điểm nằm ngoài phạm vi nội suy.")

if __name__ == "__main__":
    main()
