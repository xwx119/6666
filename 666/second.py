import streamlit as st
import pandas as pd
from io import StringIO


# ---------------------- 高级模板文案生成（无模型依赖） ----------------------
def generate_copywriting(topic, style, duration, keywords):
    # 按风格定制高级模板（不死板、有质感）
    keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
    # 补全关键词（避免索引报错）
    while len(keyword_list) < 3:
        keyword_list.append(keyword_list[-1] if keyword_list else "细节")

    style_templates = {
        "美妆": f"""【标题】{duration}精致感｜{topic}的{keyword_list[0]}美学
【正文】早起5分钟搞定的{topic}，核心是{keyword_list[0]}的哑光/清透质地，适配通勤/约会全场景。
底妆选{keyword_list[1]}款，轻薄不卡粉，搭配{keyword_list[2]}口红，持妆8小时不脱妆。
职场女性的高级感，藏在每一处不刻意的细节里。""",

        "搞笑": f"""【标题】反套路｜{topic}居然能这么玩
【正文】家人们！{duration}解锁{topic}新姿势，{keyword_list[0]}的反差感直接拉满。
本以为是普通日常，结果{keyword_list[1]}一出，松弛感拉满还不低俗。
最后这个小彩蛋，谁看了都笑但又不尬～""",

        "科普": f"""【标题】90%的人都误解了{topic}
【正文】{duration}硬核科普：{topic}的核心不是{keyword_list[0]}，而是{keyword_list[1]}。
用{keyword_list[2]}做类比，秒懂专业知识，实用又好记。
记住这个小技巧，再也不用被误导了。""",

        "励志": f"""【标题】慢慢来｜{topic}的温柔坚定
【正文】{duration}治愈向：{topic}从来不是一蹴而就，{keyword_list[0]}才是关键。
职场/生活里的{keyword_list[1]}，都是稳步成长的印记。
不必焦虑，你走的每一步都算数。""",

        "情感": f"""【标题】成年人的温柔｜藏在{topic}里
【正文】{duration}走心向：{topic}的美好，在于{keyword_list[0]}的小细节。
一个眼神、一次{keyword_list[1]}，温柔戳心却不矫情。
这就是生活最真实的美好啊。"""
    }
    return style_templates[style]


# ---------------------- 高级词汇替换 ----------------------
def load_hot_words():
    default_csv = """普通词,热门词,适用风格
分享,深度种草,美妆
好看,质感出众,美妆
开心,松弛感拉满,搞笑
知识,硬核干货,科普
努力,稳步成长,励志
感动,温柔戳心,情感
喜欢,心生偏爱,全风格
好用,实用性拉满,全风格
漂亮,氛围感十足,全风格
厉害,实力出圈,全风格
"""
    uploaded_file = st.sidebar.file_uploader("上传热门词库CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(StringIO(default_csv))
    return df


hot_words_df = load_hot_words()


def replace_hot_words(copywriting, style):
    if copywriting and not hot_words_df.empty:
        style_words = hot_words_df[(hot_words_df["适用风格"] == style) | (hot_words_df["适用风格"] == "全风格")]
        for _, row in style_words.iterrows():
            if pd.notna(row["普通词"]) and pd.notna(row["热门词"]):
                copywriting = copywriting.replace(row["普通词"], row["热门词"])
    return copywriting


# ---------------------- 界面优化 ----------------------
st.set_page_config(page_title="高级短视频文案生成器", page_icon="🎨", layout="wide")
st.title("🎨 高级短视频文案自动生成系统")

# 侧边栏
st.sidebar.title("⚙️ 生成设置")
use_hot_words = st.sidebar.checkbox("启用高级词汇替换", value=True)

# 输入区
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("🎯 视频主题", placeholder="如：秋日通勤妆容、职场高效沟通、城市治愈散步")
    style = st.selectbox("✨ 风格类型", ["美妆", "搞笑", "科普", "励志", "情感"])
with col2:
    duration = st.radio("⏱️ 视频时长", ["15s", "30s", "60s"], horizontal=True)
    keywords = st.text_input("🔑 核心关键词", placeholder="如：大地色、逻辑表达、慢生活（3-5个，用逗号分隔）")

# 生成按钮
if st.button("🚀 生成高级文案", type="primary"):
    if not topic or not keywords:
        st.warning("⚠️ 请填写主题和关键词！")
    else:
        with st.spinner("🎨 正在打磨高级文案..."):
            base_copy = generate_copywriting(topic, style, duration, keywords)
            final_copy = replace_hot_words(base_copy, style) if use_hot_words else base_copy

            # 美化展示
            formatted_copy = final_copy.replace('\n', '<br>')
            st.subheader("✅ 生成结果")
            st.markdown(f"""
            <div style="background-color:#f5f5f5; padding:20px; border-radius:8px; line-height:1.8;">
            {formatted_copy}
            </div>
            """, unsafe_allow_html=True)

            # 复制功能
            copy_js = f"""
            <script>
            const text = `{final_copy}`;
            navigator.clipboard.writeText(text).then(() => {{
                alert('✅ 高级文案已复制到剪贴板！');
            }}).catch(err => {{
                alert('❌ 复制失败：请手动选中文案复制');
            }});
            </script>
            """
            st.components.v1.html(copy_js, height=0)
            st.button("📋 复制文案", on_click=lambda: None)

# 高级提示
st.sidebar.info("""
### 高级文案技巧
1. 主题建议：加入场景（如「办公室咖啡」→「职场下午茶咖啡仪式感」）
2. 关键词：用精准词（如「美妆」用「哑光质地」而非「好看」）
3. 风格适配：美妆突出「质感」，情感突出「细节」，搞笑突出「反差」
""")