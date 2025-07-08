import streamlit as st
import pandas as pd
import os

def community_page():
    st.title("🗣️ Community Forum")
    st.write("Welcome to the mental health community space. Share thoughts, advice, or supportive messages.")
    name = st.text_input("Your Name")
    message = st.text_area("What's on your mind?")
    if st.button("Post"):
        if name and message:
            df = pd.read_csv("community_posts.csv") if os.path.exists("community_posts.csv") else pd.DataFrame(columns=["Timestamp", "Name", "Message", "Likes"])
            new_post = {
                "Timestamp": pd.to_datetime("now").strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name.strip(),
                "Message": message.strip(),
                "Likes": 0
            }
            df = pd.concat([df, pd.DataFrame([new_post])], ignore_index=True)
            df.to_csv("community_posts.csv", index=False)
            st.success("Message posted!")
            st.rerun()
        else:
            st.warning("Please enter both name and message.")

    posts_df = pd.read_csv("community_posts.csv") if os.path.exists("community_posts.csv") else pd.DataFrame(columns=["Timestamp", "Name", "Message", "Likes"])
    replies_df = pd.read_csv("community_replies.csv") if os.path.exists("community_replies.csv") else pd.DataFrame(columns=["PostTimestamp", "Replier", "Reply"])

    if not posts_df.empty:
        st.subheader("📝 Recent Posts")
        posts_df = posts_df.sort_values(by="Timestamp", ascending=False)

        for idx, row in posts_df.iterrows():
            st.markdown("---")
            st.markdown(f"**{row['Name']}** *({row['Timestamp']})*")
            st.markdown(f"> {row['Message']}")

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("👍", key=f"like_{idx}"):
                    posts_df.at[idx, "Likes"] += 1
                    posts_df.to_csv("community_posts.csv", index=False)
                    st.rerun()
            with col2:
                st.write(f"Likes: {row['Likes']}")

            post_replies = replies_df[replies_df["PostTimestamp"] == row["Timestamp"]]
            for _, reply in post_replies.iterrows():
                st.markdown(f"↪️ **{reply['Replier']}**: {reply['Reply']}")

            with st.expander("💬 Reply"):
                replier = st.text_input(f"Reply Name {idx}", label_visibility="collapsed", placeholder="Your name")
                reply_text = st.text_area(f"Reply Text {idx}", label_visibility="collapsed", placeholder="Your reply...")
                if st.button(f"Post Reply {idx}"):
                    if replier.strip() and reply_text.strip():
                        new_reply = {
                            "PostTimestamp": row["Timestamp"],
                            "Replier": replier.strip(),
                            "Reply": reply_text.strip()
                        }
                        replies_df = pd.concat([replies_df, pd.DataFrame([new_reply])], ignore_index=True)
                        replies_df.to_csv("community_replies.csv", index=False)
                        st.success("Reply posted!")
                        st.rerun()