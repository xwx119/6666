import streamlit as st
import pandas as pd
from io import StringIO


# ---------------------- 无模型依赖：直接返回示例文案 ----------------------
def generate_copywriting(topic, style, duration, keywords):
    # 示例文案模板，无需模型
    examples = {
        "美妆": f"【标题】{topic}绝绝子！{keywords.split(',')[0]}太香了\n【正文】宝子们！{duration}快速安利{topic}，{keywords}直接拉满，谁用谁好看！",
        "搞笑": f"【标题】笑不活了！{topic}居然这么玩\n【正文】家人们谁懂啊！{duration}整活{topic}，{keywords}直接封神，笑到肚子疼！",
        "科普": f"【标题】{topic}干货！90%的人都搞错了\n【正文】{duration}硬核科普{topic}，记住{keywords}，轻松搞定！",
        "励志": f"【标题】{topic}冲鸭！你只管努力\n【正文】{duration}励志向！{topic}的核心是{keywords}，坚持就会有收获！",
        "情感": f"【标题】破防了！{topic}戳中泪点\n【正文】{duration}走心分享{topic}，{keywords}这几个瞬间，有没有想起自己？"
    }
    return examples.get(style, f"【标题】{topic}\n【正文】{duration} {style}风格{topic}，关键词：{keywords}")


# ---------------------- 热门词替换（保持不变） ----------------------
def load_hot_words():
    default_csv = """普通词,热门词,适用风格
分享,安利,美妆
好看,绝绝子,美妆
开心,美滋滋,搞笑
知识,干货,科普
努力,冲鸭,励志
感动,破防了,情感
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
        style_words = hot_words_df[hot_words_df["适用风格"] == style]
        for _, row in style_words.iterrows():
            if pd.notna(row["普通词"]) and pd.notna(row["热门词"]):
                copywriting = copywriting.replace(row["普通词"], row["热门词"])
    return copywriting


# ---------------------- Streamlit界面 ----------------------
st.set_page_config(page_title="短视频文案生成器", page_icon="📝", layout="wide")
st.title("📝 短视频文案自动生成系统")

# 侧边栏
st.sidebar.title("⚙️ 设置")
use_hot_words = st.sidebar.checkbox("启用热门词替换", value=True)

# 输入区
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("🎯 视频主题", placeholder="如：秋季穿搭分享、职场干货、美食教程")
    style = st.selectbox("✨ 风格类型", ["搞笑", "科普", "情感", "励志", "美妆"])
with col2:
    duration = st.radio("⏱️ 视频时长", ["15s", "30s", "60s"], horizontal=True)
    keywords = st.text_input("🔑 关键词", placeholder="请输入3-5个核心词，用逗号分隔")

# 生成按钮
if st.button("🚀 生成文案", type="primary"):
    if not topic or not keywords:
        st.warning("⚠️ 请填写主题和关键词！")
    else:
        with st.spinner("🤖 正在生成文案..."):
            base_copy = generate_copywriting(topic, style, duration, keywords)
            final_copy = replace_hot_words(base_copy, style) if use_hot_words else base_copy

            # 展示结果
            st.subheader("✅ 生成结果")
            st.text_area("", value=final_copy, height=200)

            # 复制功能
            copy_js = f"""
            <script>
            const text = `{final_copy}`;
            navigator.clipboard.writeText(text).then(() => {{
                alert('✅ 文案已复制到剪贴板！');
            }}).catch(err => {{
                alert('❌ 复制失败：手动复制即可');
            }});
            </script>
            """
            st.components.v1.html(copy_js, height=0)
            st.button("📋 复制文案", on_click=lambda: None)