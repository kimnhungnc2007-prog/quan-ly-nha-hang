import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hệ Thống Tính Tiền Trà Sữa",
    page_icon="🧋",
    layout="wide"
)

# Ảnh TRASUA.jpg cần nằm cùng thư mục với app.py
try:
    st.image("TRASUA.jpg", use_container_width=True)
except Exception:
    st.caption("🧋 BOBA TEA - TRÀ SỮA MR BÌNH")

# ---------------------------------------------------------
# 2. MENU TRÀ SỮA
# ---------------------------------------------------------
MENU_TEA = {
    "Trà Sữa Truyền Thống": 30000,
    "Trà Sữa Trân Châu Đường Đen": 35000,
    "Trà Sữa Thái Xanh": 32000,
    "Trà Sữa Ô Long": 35000,
    "Trà Sữa Matcha": 38000,
    "Trà Sữa Dâu Tây": 35000,
    "Trà Đào Cam Sả": 35000,
    "Trà Dâu Tằm": 32000,
}

SIZE_OPTIONS = {
    "S (Vừa)": 0,
    "M (Lớn)": 5000,
    "L (Đặc biệt)": 10000
}

TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}

SUGAR_LEVELS = [
    "100% (Bình thường)", "70%", "50%", "30%",
    "0% (Không đường)"
]
ICE_LEVELS = [
    "100% (Bình thường)", "70%", "50%", "30%",
    "0% (Không đá)"
]

# ---------------------------------------------------------
# 3. MENU ĐỒ ĂN VẶT
# Giá bán được thiết lập mẫu, có thể thay đổi
# ---------------------------------------------------------
MENU_SNACK = {
    "Khoai tây chiên": 25000,
    "Phô mai que": 30000,
    "Gà viên chiên": 30000,
    "Xúc xích chiên": 20000,
    "Bánh tráng trộn": 25000,
    "Bánh tráng cuốn": 25000,
    "Cá viên chiên": 25000,
    "Khô gà lá chanh": 30000,
    "Bánh mochi": 20000,
    "Bánh waffle": 30000,
    "Bánh flan": 12000,
    "Bánh quy bơ": 18000,
}

# ---------------------------------------------------------
# 4. QUY TẮC ĐỀ XUẤT MÓN ĂN VẶT
# ---------------------------------------------------------
SNACK_RECOMMENDATIONS = {
    "Trà Sữa Truyền Thống": [
        "Khoai tây chiên",
        "Phô mai que",
        "Bánh flan",
    ],
    "Trà Sữa Trân Châu Đường Đen": [
        "Bánh mochi",
        "Bánh quy bơ",
        "Phô mai que",
    ],
    "Trà Sữa Thái Xanh": [
        "Bánh waffle",
        "Bánh flan",
        "Khoai tây chiên",
    ],
    "Trà Sữa Ô Long": [
        "Khô gà lá chanh",
        "Bánh quy bơ",
        "Cá viên chiên",
    ],
    "Trà Sữa Matcha": [
        "Bánh mochi",
        "Bánh waffle",
        "Bánh quy bơ",
    ],
    "Trà Sữa Dâu Tây": [
        "Bánh waffle",
        "Bánh mochi",
        "Phô mai que",
    ],
    "Trà Đào Cam Sả": [
        "Bánh tráng trộn",
        "Khoai tây chiên",
        "Xúc xích chiên",
    ],
    "Trà Dâu Tằm": [
        "Bánh tráng cuốn",
        "Cá viên chiên",
        "Bánh quy bơ",
    ],
}

# ---------------------------------------------------------
# 5. KHỞI TẠO SESSION STATE
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False

if "invoice_data" not in st.session_state:
    st.session_state.invoice_data = None

# ---------------------------------------------------------
# 6. HÀM THÊM MÓN VÀO GIỎ
# ---------------------------------------------------------
def add_to_cart(
    name, category, unit_price, quantity,
    size="-", sugar="-", ice="-", topping="Không"
):
    item = {
        "Nhóm món": category,
        "Tên món": name,
        "Size": size,
        "Đường": sugar,
        "Đá": ice,
        "Topping": topping,
        "Đơn giá": int(unit_price),
        "Số lượng": int(quantity),
        "Thành tiền": int(unit_price) * int(quantity),
    }

    st.session_state.cart.append(item)
    st.session_state.invoice_paid = False
    st.session_state.invoice_data = None

# ---------------------------------------------------------
# 7. HÀM TẠO HÓA ĐƠN TXT
# ---------------------------------------------------------
def create_txt_invoice(
    customer_name, cart, total_amount, discount, final_amount, paid_at
):
    content = "=" * 45 + "\n"
    content += "HÓA ĐƠN BÁN HÀNG - MR BÌNH\n"
    content += "=" * 45 + "\n"
    content += f"Ngày: {paid_at}\n"
    content += (
        f"Khách hàng: {customer_name or 'Khách vãng lai'}\n"
    )
    content += "-" * 45 + "\n"

    for idx, item in enumerate(cart, 1):
        content += (
            f"{idx}. [{item['Nhóm món']}] {item['Tên món']}\n"
        )
        if item["Size"] != "-":
            content += f"   Size: {item['Size']}\n"
            content += (
                f"   Đường: {item['Đường']} | "
                f"Đá: {item['Đá']}\n"
            )

        if item["Topping"] != "Không":
            content += f"   Topping: {item['Topping']}\n"

        content += (
            f"   SL: {item['Số lượng']} x "
            f"{item['Đơn giá']:,} = "
            f"{item['Thành tiền']:,} VNĐ\n"
        )

    content += "-" * 45 + "\n"
    content += f"Tổng tiền: {total_amount:,} VNĐ\n"
    content += f"Giảm giá: {discount}%\n"
    content += f"THANH TOÁN: {final_amount:,} VNĐ\n"
    content += "=" * 45 + "\n"
    content += "Cảm ơn quý khách và hẹn gặp lại!\n"

    return content

# ---------------------------------------------------------
# 8. GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.title("🧋 QUÁN TRÀ SỮA MR BÌNH")
st.caption("Trà sữa ngon - Ăn vặt vui - Phục vụ tận tâm")
st.divider()

col_left, col_right = st.columns([1.1, 0.9])

# =========================================================
# CỘT TRÁI: CHỌN MÓN
# =========================================================
with col_left:
    st.subheader("📝 Thông tin đơn hàng")

    customer_name = st.text_input(
        "Tên khách hàng",
        placeholder="Nhập tên khách hàng..."
    )

    st.markdown("### 🧋 Chọn trà sữa")

    col_item, col_qty = st.columns([3, 1])

    with col_item:
        selected_tea = st.selectbox(
            "Loại trà sữa",
            list(MENU_TEA.keys())
        )

    with col_qty:
        quantity = st.number_input(
            "Số lượng ly",
            min_value=1,
            value=1,
            step=1,
            key="tea_quantity"
        )

    c_size, c_sugar, c_ice = st.columns(3)

    with c_size:
        selected_size = st.selectbox(
            "Size",
            list(SIZE_OPTIONS.keys())
        )

    with c_sugar:
        selected_sugar = st.selectbox(
            "Mức đường",
            SUGAR_LEVELS
        )

    with c_ice:
        selected_ice = st.selectbox(
            "Mức đá",
            ICE_LEVELS
        )

    selected_toppings = st.multiselect(
        "Chọn topping",
        list(TOPPING_OPTIONS.keys())
    )

    base_price = MENU_TEA[selected_tea]
    size_price = SIZE_OPTIONS[selected_size]
    topping_price = sum(
        TOPPING_OPTIONS[t] for t in selected_toppings
    )
    unit_price = base_price + size_price + topping_price
    item_total = unit_price * quantity

    st.info(
        f"Đơn giá: {unit_price:,} VNĐ/ly\n\n"
        f"Thành tiền: {item_total:,} VNĐ"
    )

    if st.button(
        "➕ Thêm trà sữa vào hóa đơn",
        type="primary",
        use_container_width=True
    ):
        topping_str = (
            ", ".join(selected_toppings)
            if selected_toppings else "Không"
        )

        add_to_cart(
            name=selected_tea,
            category="Trà sữa",
            unit_price=unit_price,
            quantity=quantity,
            size=selected_size.split()[0],
            sugar=selected_sugar.split()[0],
            ice=selected_ice.split()[0],
            topping=topping_str
        )

        st.toast("Đã thêm trà sữa vào giỏ hàng!", icon="✅")

    # -----------------------------------------------------
    # TÍNH NĂNG MỚI: ĐỀ XUẤT MÓN ĂN VẶT
    # -----------------------------------------------------
    st.divider()
    st.subheader("🍟 Gợi ý món ăn vặt ăn kèm")

    st.write(
        f"Khách chọn **{selected_tea}**. "
        "Bạn có thể tham khảo các món ăn kèm sau:"
    )

    recommended_snacks = SNACK_RECOMMENDATIONS.get(
        selected_tea, list(MENU_SNACK.keys())[:3]
    )

    for snack in recommended_snacks:
        with st.container(border=True):
            snack_col, button_col = st.columns([3, 1])

            with snack_col:
                st.markdown(f"**🍴 {snack}**")
                st.caption(f"Giá: {MENU_SNACK[snack]:,} VNĐ")

            with button_col:
                if st.button(
                    "Thêm",
                    key=f"add_snack_{snack}",
                    use_container_width=True
                ):
                    add_to_cart(
                        name=snack,
                        category="Ăn vặt",
                        unit_price=MENU_SNACK[snack],
                        quantity=1
                    )
                    st.toast(
                        f"Đã thêm {snack} vào giỏ!",
                        icon="🥡"
                    )

    with st.expander("📋 Xem toàn bộ menu ăn vặt"):
        snack_name = st.selectbox(
            "Chọn món ăn vặt",
            list(MENU_SNACK.keys()),
            key="all_snack_select"
        )

        snack_qty = st.number_input(
            "Số phần",
            min_value=1,
            value=1,
            step=1,
            key="snack_quantity"
        )

        st.write(
            f"Thành tiền: "
            f"{MENU_SNACK[snack_name] * snack_qty:,} VNĐ"
        )

        if st.button(
            "➕ Thêm món ăn vặt đã chọn",
            use_container_width=True
        ):
            add_to_cart(
                name=snack_name,
                category="Ăn vặt",
                unit_price=MENU_SNACK[snack_name],
                quantity=snack_qty
            )
            st.toast("Đã thêm món ăn vặt!", icon="✅")

# =========================================================
# CỘT PHẢI: GIỎ HÀNG VÀ THANH TOÁN
# =========================================================
with col_right:
    st.subheader("🛒 Giỏ hàng")

    if not st.session_state.cart:
        st.warning("Giỏ hàng đang trống. Hãy chọn món!")
    else:
        df_cart = pd.DataFrame(st.session_state.cart)

        st.dataframe(
            df_cart[
                [
                    "Nhóm món", "Tên món", "Size", "Topping",
                    "Số lượng", "Đơn giá", "Thành tiền"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Số dòng món hàng: {len(st.session_state.cart)}"
        )

        col_clear, col_remove = st.columns(2)

        with col_clear:
            if st.button(
                "🗑️ Xóa toàn bộ",
                use_container_width=True
            ):
                st.session_state.cart = []
                st.session_state.invoice_paid = False
                st.session_state.invoice_data = None
                st.rerun()

        with col_remove:
            if st.button(
                "↩️ Bỏ món cuối",
                use_container_width=True
            ):
                st.session_state.cart.pop()
                st.session_state.invoice_paid = False
                st.session_state.invoice_data = None
                st.rerun()

        st.divider()

        total_price = sum(
            item["Thành tiền"]
            for item in st.session_state.cart
        )

        discount = st.number_input(
            "Giảm giá (%)",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
            key="discount"
        )

        final_price = int(
            total_price * (1 - discount / 100)
        )

        st.markdown(
            f"### Tổng tiền: {total_price:,} VNĐ"
        )

        if discount > 0:
            st.markdown(
                f"### Sau giảm giá: {final_price:,} VNĐ"
            )

        st.markdown(
            f"**Tiết kiệm:** "
            f"{total_price - final_price:,} VNĐ"
        )

        if st.button(
            "💳 XÁC NHẬN THANH TOÁN",
            type="primary",
            use_container_width=True
        ):
            paid_at = datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )

            # Lưu bản chụp hóa đơn để không thay đổi
            st.session_state.invoice_data = {
                "customer_name": customer_name,
                "cart": [
                    item.copy()
                    for item in st.session_state.cart
                ],
                "total_price": total_price,
                "discount": discount,
                "final_price": final_price,
                "paid_at": paid_at
            }

            st.session_state.invoice_paid = True
            st.balloons()
            st.rerun()

# =========================================================
# 9. HIỂN THỊ VÀ TẢI HÓA ĐƠN
# =========================================================
if (
    st.session_state.invoice_paid
    and st.session_state.invoice_data
):
    invoice = st.session_state.invoice_data

    st.divider()
    st.success("🎉 Thanh toán thành công!")

    with st.container(border=True):
        st.markdown(
            "<h2 style='text-align:center;color:#FF4B4B'>"
            "🧋 HÓA ĐƠN BÁN HÀNG - MR BÌNH"
            "</h2>",
            unsafe_allow_html=True
        )

        st.write(f"**Thời gian:** {invoice['paid_at']}")
        st.write(
            "**Khách hàng:** "
            f"{invoice['customer_name'] or 'Khách vãng lai'}"
        )

        invoice_df = pd.DataFrame(invoice["cart"])

        st.dataframe(
            invoice_df[
                [
                    "Nhóm món", "Tên món", "Size", "Đường",
                    "Đá", "Topping", "Số lượng", "Đơn giá",
                    "Thành tiền"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        c1, c2 = st.columns(2)

        with c1:
            st.write(
                f"**Tổng tiền:** "
                f"{invoice['total_price']:,} VNĐ"
            )
            st.write(
                f"**Giảm giá:** {invoice['discount']}%"
            )

        with c2:
            st.markdown(
                f"### Thanh toán: "
                f"{invoice['final_price']:,} VNĐ"
            )

    txt_data = create_txt_invoice(
        invoice["customer_name"],
        invoice["cart"],
        invoice["total_price"],
        invoice["discount"],
        invoice["final_price"],
        invoice["paid_at"]
    )

    filename = (
        "HoaDon_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".txt"
    )

    st.download_button(
        "📥 Tải hóa đơn TXT",
        data=txt_data,
        file_name=filename,
        mime="text/plain",
        use_container_width=True
    )

    if st.button(
        "🔄 Tạo đơn hàng mới",
        use_container_width=True
    ):
        st.session_state.cart = []
        st.session_state.invoice_paid = False
        st.session_state.invoice_data = None
        st.rerun()
