import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
from datetime import datetime

# =====================================================
# 1. CẤU HÌNH
# =====================================================
st.set_page_config(
    page_title="Trà Sữa MR BÌNH",
    page_icon="🧋",
    layout="wide"
)

# =====================================================
# 2. MENU VÀ GIÁ
# =====================================================
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
    "L (Đặc biệt)": 10000,
}

TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000,
}

SUGAR_LEVELS = [
    "100% (Bình thường)", "70%", "50%", "30%", "0% (Không đường)"
]
ICE_LEVELS = [
    "100% (Bình thường)", "70%", "50%", "30%", "0% (Không đá)"
]

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

# =====================================================
# 3. HÌNH ẢNH MINH HỌA
# Bạn có thể thay URL bằng ảnh thật của quán.
# =====================================================
TEA_IMAGES = {
    "Trà Sữa Truyền Thống":
        "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=600&q=80",
    "Trà Sữa Trân Châu Đường Đen":
        "https://images.unsplash.com/photo-1525385133512-2f3bdd039054?auto=format&fit=crop&w=600&q=80",
    "Trà Sữa Thái Xanh":
        "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=600&q=80",
    "Trà Sữa Ô Long":
        "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=600&q=80",
    "Trà Sữa Matcha":
        "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=600&q=80",
    "Trà Sữa Dâu Tây":
        "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?auto=format&fit=crop&w=600&q=80",
    "Trà Đào Cam Sả":
        "https://images.unsplash.com/photo-1513558161293-cdaf765edfd7?auto=format&fit=crop&w=600&q=80",
    "Trà Dâu Tằm":
        "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=600&q=80",
}

SNACK_IMAGES = {
    "Khoai tây chiên":
        "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=600&q=80",
    "Phô mai que":
        "https://images.unsplash.com/photo-1531749668029-2db88e4276c7?auto=format&fit=crop&w=600&q=80",
    "Gà viên chiên":
        "https://images.unsplash.com/photo-1562967914-608f82629710?auto=format&fit=crop&w=600&q=80",
    "Xúc xích chiên":
        "https://images.unsplash.com/photo-1526367790999-0150786686a2?auto=format&fit=crop&w=600&q=80",
    "Bánh tráng trộn":
        "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=600&q=80",
    "Bánh tráng cuốn":
        "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80",
    "Cá viên chiên":
        "https://images.unsplash.com/photo-1562967916-eb82221dfb92?auto=format&fit=crop&w=600&q=80",
    "Khô gà lá chanh":
        "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=600&q=80",
    "Bánh mochi":
        "https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=600&q=80",
    "Bánh waffle":
        "https://images.unsplash.com/photo-1562376552-0d160a2f238d?auto=format&fit=crop&w=600&q=80",
    "Bánh flan":
        "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=600&q=80",
    "Bánh quy bơ":
        "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=600&q=80",
}

# =====================================================
# 4. GỢI Ý ĂN VẶT
# =====================================================
SNACK_RECOMMENDATIONS = {
    "Trà Sữa Truyền Thống": [
        "Khoai tây chiên", "Phô mai que", "Bánh flan"
    ],
    "Trà Sữa Trân Châu Đường Đen": [
        "Bánh mochi", "Bánh quy bơ", "Phô mai que"
    ],
    "Trà Sữa Thái Xanh": [
        "Bánh waffle", "Bánh flan", "Khoai tây chiên"
    ],
    "Trà Sữa Ô Long": [
        "Khô gà lá chanh", "Bánh quy bơ", "Cá viên chiên"
    ],
    "Trà Sữa Matcha": [
        "Bánh mochi", "Bánh waffle", "Bánh quy bơ"
    ],
    "Trà Sữa Dâu Tây": [
        "Bánh waffle", "Bánh mochi", "Phô mai que"
    ],
    "Trà Đào Cam Sả": [
        "Bánh tráng trộn", "Khoai tây chiên", "Xúc xích chiên"
    ],
    "Trà Dâu Tằm": [
        "Bánh tráng cuốn", "Cá viên chiên", "Bánh quy bơ"
    ],
}

# =====================================================
# 5. VÒNG QUAY MAY MẮN
# Các phần thưởng được chọn ngẫu nhiên với xác suất bằng nhau.
# =====================================================
PRIZES = [
    {"label": "Chúc bạn may mắn lần sau", "discount": 0},
    {"label": "Giảm 5%", "discount": 5},
    {"label": "Giảm 10%", "discount": 10},
    {"label": "Giảm 15%", "discount": 15},
    {"label": "Giảm 20%", "discount": 20},
    {"label": "Giảm 5%", "discount": 5},
]

# =====================================================
# 6. SESSION STATE
# =====================================================
defaults = {
    "cart": [],
    "invoice_paid": False,
    "invoice_data": None,
    "promo_discount": 0,
    "promo_result": None,
    "promo_used": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================================
# 7. HÀM XỬ LÝ
# =====================================================
def add_to_cart(
    name, category, price, quantity,
    size="-", sugar="-", ice="-", topping="Không"
):
    st.session_state.cart.append({
        "Nhóm món": category,
        "Tên món": name,
        "Size": size,
        "Đường": sugar,
        "Đá": ice,
        "Topping": topping,
        "Đơn giá": int(price),
        "Số lượng": int(quantity),
        "Thành tiền": int(price) * int(quantity),
    })
    st.session_state.invoice_paid = False
    st.session_state.invoice_data = None


def reset_order():
    st.session_state.cart = []
    st.session_state.invoice_paid = False
    st.session_state.invoice_data = None
    st.session_state.promo_discount = 0
    st.session_state.promo_result = None
    st.session_state.promo_used = False


def create_invoice_text(invoice):
    lines = [
        "=" * 44,
        "HÓA ĐƠN BÁN HÀNG - TRÀ SỮA MR BÌNH",
        "=" * 44,
        f"Thời gian: {invoice['paid_at']}",
        f"Khách hàng: {invoice['customer'] or 'Khách vãng lai'}",
        "-" * 44,
    ]

    for i, item in enumerate(invoice["cart"], 1):
        lines.append(
            f"{i}. [{item['Nhóm món']}] {item['Tên món']}"
        )
        if item["Size"] != "-":
            lines.append(
                f"   Size {item['Size']} | Đường {item['Đường']} "
                f"| Đá {item['Đá']}"
            )
        if item["Topping"] != "Không":
            lines.append(f"   Topping: {item['Topping']}")
        lines.append(
            f"   {item['Số lượng']} x {item['Đơn giá']:,} "
            f"= {item['Thành tiền']:,} VNĐ"
        )

    lines += [
        "-" * 44,
        f"Tổng tiền: {invoice['total']:,} VNĐ",
        f"Giảm giá: {invoice['discount']}%",
        f"Thành tiền: {invoice['final']:,} VNĐ",
        "=" * 44,
        "Cảm ơn quý khách và hẹn gặp lại!",
    ]
    return "\n".join(lines)


# =====================================================
# 8. ĐẦU TRANG
# =====================================================
try:
    st.image("TRASUA.jpg", use_container_width=True)
except Exception:
    st.markdown("# 🧋 TRÀ SỮA MR BÌNH")

st.title("🧋 QUÁN TRÀ SỮA MR BÌNH")
st.caption("Trà sữa ngon • Ăn vặt vui • Khuyến mãi hấp dẫn")
st.divider()

# =====================================================
# 9. VÒNG QUAY KHUYẾN MÃI
# =====================================================
st.subheader("🎡 Vòng quay may mắn")
st.write(
    "Mỗi đơn hàng được quay một lần. "
    "Ưu đãi sẽ được áp dụng vào hóa đơn hiện tại."
)

wheel_col, prize_col = st.columns([1.2, 1])

with wheel_col:
    labels = [p["label"] for p in PRIZES]
    colors = [
        "#F94144", "#F3722C", "#F9C74F",
        "#90BE6D", "#43AA8B", "#577590"
    ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=[1] * len(PRIZES),
                hole=0,
                sort=False,
                direction="clockwise",
                marker=dict(
                    colors=colors,
                    line=dict(color="white", width=3)
                ),
                textinfo="label",
                textposition="inside",
                insidetextorientation="radial",
            )
        ]
    )

    fig.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=350,
    )

    st.plotly_chart(fig, use_container_width=True)

with prize_col:
    st.markdown("### 🎁 Cơ hội nhận ưu đãi")
    st.markdown("- Không trúng giảm giá")
    st.markdown("- Giảm 5%")
    st.markdown("- Giảm 10%")
    st.markdown("- Giảm 15%")
    st.markdown("- Giảm 20%")

    if st.session_state.promo_used:
        st.success(
            f"🎉 Kết quả: {st.session_state.promo_result}"
        )
        st.metric(
            "Ưu đãi vòng quay",
            f"{st.session_state.promo_discount}%"
        )
    elif st.button(
        "🎡 QUAY NGAY",
        type="primary",
        use_container_width=True,
    ):
        prize = random.choice(PRIZES)
        st.session_state.promo_result = prize["label"]
        st.session_state.promo_discount = prize["discount"]
        st.session_state.promo_used = True
        st.rerun()

    if st.session_state.promo_used:
        if st.session_state.promo_discount > 0:
            st.info(
                "Ưu đãi sẽ tự động áp dụng vào hóa đơn."
            )
        else:
            st.caption("Bạn có thể thử vận may ở đơn hàng sau.")

st.divider()

# =====================================================
# 10. CHỌN TRÀ SỮA VÀ ĐỒ ĂN
# =====================================================
left, right = st.columns([1.1, 0.9])

with left:
    st.subheader("🧋 Chọn trà sữa")

    customer = st.text_input(
        "Tên khách hàng",
        placeholder="Nhập tên khách hàng..."
    )

    selected_tea = st.selectbox(
        "Loại trà sữa", list(MENU_TEA.keys())
    )

    tea_image = TEA_IMAGES.get(selected_tea)
    if tea_image:
        st.image(
            tea_image,
            caption=selected_tea,
            use_container_width=True
        )

    c1, c2, c3 = st.columns(3)

    with c1:
        size = st.selectbox("Size", list(SIZE_OPTIONS.keys()))

    with c2:
        sugar = st.selectbox("Đường", SUGAR_LEVELS)

    with c3:
        ice = st.selectbox("Đá", ICE_LEVELS)

    tea_qty = st.number_input(
        "Số lượng ly",
        min_value=1,
        value=1,
        step=1,
        key="tea_qty"
    )

    toppings = st.multiselect(
        "Topping",
        list(TOPPING_OPTIONS.keys())
    )

    tea_unit = (
        MENU_TEA[selected_tea]
        + SIZE_OPTIONS[size]
        + sum(TOPPING_OPTIONS[t] for t in toppings)
    )

    st.info(
        f"Đơn giá: {tea_unit:,} VNĐ/ly\n\n"
        f"Thành tiền: {tea_unit * tea_qty:,} VNĐ"
    )

    if st.button(
        "➕ Thêm trà sữa",
        type="primary",
        use_container_width=True
    ):
        add_to_cart(
            selected_tea,
            "Trà sữa",
            tea_unit,
            tea_qty,
            size.split()[0],
            sugar.split()[0],
            ice.split()[0],
            ", ".join(toppings) if toppings else "Không"
        )
        st.toast("Đã thêm trà sữa!", icon="✅")

    st.divider()
    st.subheader("🍟 Món ăn vặt đề xuất")

    recommendations = SNACK_RECOMMENDATIONS[selected_tea]
    st.caption(f"Gợi ý ăn kèm với {selected_tea}")

    snack_cols = st.columns(3)

    for i, snack in enumerate(recommendations):
        with snack_cols[i]:
            image_url = SNACK_IMAGES.get(snack)
            if image_url:
                st.image(image_url, use_container_width=True)

            st.markdown(f"**{snack}**")
            st.write(f"{MENU_SNACK[snack]:,} đ")

            if st.button(
                "Thêm món",
                key=f"recommend_{snack}",
                use_container_width=True
            ):
                add_to_cart(
                    snack, "Ăn vặt",
                    MENU_SNACK[snack], 1
                )
                st.toast(f"Đã thêm {snack}!", icon="🥡")

    with st.expander("📋 Xem toàn bộ menu ăn vặt"):
        snack = st.selectbox(
            "Chọn món",
            list(MENU_SNACK.keys()),
            key="all_snacks"
        )

        image_url = SNACK_IMAGES.get(snack)
        if image_url:
            st.image(image_url, width=240)

        st.write(f"Giá: {MENU_SNACK[snack]:,} VNĐ")

        snack_qty = st.number_input(
            "Số phần",
            min_value=1,
            value=1,
            step=1,
            key="snack_qty"
        )

        if st.button("➕ Thêm món ăn vặt"):
            add_to_cart(
                snack, "Ăn vặt",
                MENU_SNACK[snack], snack_qty
            )
            st.toast("Đã thêm món ăn vặt!", icon="✅")

# =====================================================
# 11. GIỎ HÀNG VÀ THANH TOÁN
# =====================================================
with right:
    st.subheader("🛒 Giỏ hàng")

    if not st.session_state.cart:
        st.info("Chưa có món nào trong hóa đơn.")
    else:
        df = pd.DataFrame(st.session_state.cart)

        st.dataframe(
            df[
                [
                    "Nhóm món", "Tên món", "Size",
                    "Số lượng", "Đơn giá", "Thành tiền"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        b1, b2 = st.columns(2)

        with b1:
            if st.button("🗑️ Xóa toàn bộ", use_container_width=True):
                st.session_state.cart = []
                st.session_state.invoice_paid = False
                st.session_state.invoice_data = None
                st.rerun()

        with b2:
            if st.button("↩️ Bỏ món cuối", use_container_width=True):
                st.session_state.cart.pop()
                st.session_state.invoice_paid = False
                st.session_state.invoice_data = None
                st.rerun()

        total = sum(
            item["Thành tiền"]
            for item in st.session_state.cart
        )

        st.divider()
        st.metric("Tổng tiền trước giảm", f"{total:,} VNĐ")

        promo_discount = st.session_state.promo_discount

        st.write(
            f"🎁 Giảm từ vòng quay: **{promo_discount}%**"
        )

        manual_discount = st.number_input(
            "Giảm giá thêm của nhân viên (%)",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
            key="manual_discount"
        )

        # Cộng ưu đãi vòng quay và ưu đãi nhân viên,
        # giới hạn tổng mức giảm tối đa 100%.
        discount = min(100, promo_discount + manual_discount)
        final_total = int(total * (1 - discount / 100))

        st.markdown(f"### Tổng giảm giá: {discount}%")
        st.markdown(f"### 💰 Cần thanh toán: {final_total:,} VNĐ")

        if st.button(
            "💳 XÁC NHẬN THANH TOÁN",
            type="primary",
            use_container_width=True
        ):
            st.session_state.invoice_data = {
                "customer": customer,
                "cart": [x.copy() for x in st.session_state.cart],
                "total": total,
                "discount": discount,
                "final": final_total,
                "paid_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
            st.session_state.invoice_paid = True
            st.balloons()
            st.rerun()

# =====================================================
# 12. HÓA ĐƠN VÀ TẢI TXT
# =====================================================
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
            "🧋 HÓA ĐƠN MR BÌNH"
            "</h2>",
            unsafe_allow_html=True
        )

        st.write(f"**Thời gian:** {invoice['paid_at']}")
        st.write(
            f"**Khách hàng:** {invoice['customer'] or 'Khách vãng lai'}"
        )

        st.dataframe(
            pd.DataFrame(invoice["cart"]),
            use_container_width=True,
            hide_index=True
        )

        st.write(f"**Tổng tiền:** {invoice['total']:,} VNĐ")
        st.write(f"**Giảm giá:** {invoice['discount']}%")
        st.markdown(f"## Thanh toán: {invoice['final']:,} VNĐ")

    txt = create_invoice_text(invoice)

    st.download_button(
        "📥 Tải hóa đơn TXT",
        data=txt,
        file_name=(
            "HoaDon_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".txt"
        ),
        mime="text/plain",
        use_container_width=True
    )

    if st.button("🔄 Tạo đơn hàng mới"):
        reset_order()
        st.rerun()
