import streamlit as st
import os
import firebase_config
from firebase_admin import firestore
from analysis import extract_text_from_pdf, personality_prediction_traits, plot_personality_traits_scores

# Get Firestore reference
db = firebase_config.db

def store_resume_in_firestore(file_name, text):
    try:
        doc_ref = db.collection("resumes").document(file_name)
        doc_ref.set({"file_name": file_name, "content": text})
        st.success("✅ Resume stored in Firebase successfully!")
    except Exception as e:
        st.error(f"❌ Failed to store resume: {str(e)}")


# Streamlit App UI
def main():

    st.set_page_config(page_title="AI Resume Personality Insights", page_icon="🧠", layout="centered")

    # Sidebar for additional information
    st.sidebar.title("🔍 About the App")
    st.sidebar.info("This AI-powered tool analyzes your resume and predicts your personality based on the Big Five traits.")

    st.sidebar.title("📌 How to Use")
    st.sidebar.write("1. Upload your resume (PDF format).")
    st.sidebar.write("2. The AI will analyze your personality traits.")
    st.sidebar.write("3. View your results and insights.")

    st.sidebar.title("📘 About the Big Five Model")
    st.sidebar.write("The Big Five Personality Traits are widely used in psychology to describe human behavior.")
    st.sidebar.write("This analysis can give insights into your professional strengths and tendencies.")
    
    # Custom Styling
    st.markdown("""
        <style>
        .stApp { background-color: #f4f4f9; }
        .big-font { font-size:24px !important; font-weight:bold; color: #4a4a4a; }
        .small-font { font-size:18px !important; color: #666666; }
        .stMarkdown h2 { color: #ff4b4b; }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='big-font'>📄 AI Resume Personality Insight</h2>", unsafe_allow_html=True)
    st.markdown("<p class='small-font'>Upload your resume and get personality insights based on the Big Five traits.</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📂 Upload Your Resume (PDF)", type=["pdf"])
    
    if uploaded_file is not None:
        file_path = f"temp_{uploaded_file.name}"
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success("✅ Resume uploaded successfully!")
        
        # Extract text from resume
        text = extract_text_from_pdf(file_path)

        # Store in Firebase
        store_resume_in_firestore(uploaded_file.name, text)

        
        # Get personality scores
        _, scores = personality_prediction_traits(text)  # Extract only the scores from the tuple
        scores = scores.tolist()  # Convert NumPy array to a normal Python list
        
        # Display results
        st.markdown("<h3 class='big-font'>📊 Personality Analysis Result</h3>", unsafe_allow_html=True)
        st.write("### Big Five Personality Scores:")
        
        labels = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
        personality_dict = dict(zip(labels, scores))  

        for trait, score in personality_dict.items():
            normalized_score = min(max(float(score), 0), 1)  # Convert to float and normalize
            st.progress(normalized_score)
            st.write(f"**{trait}:** {score:.2f}")


        # Plot the personality traits visualization
        st.markdown("<h3 class='big-font'>📈 Personality Traits Visualization</h3>", unsafe_allow_html=True)
        fig = plot_personality_traits_scores(scores)  # ✅ Call function and get figure
        st.pyplot(fig)  # ✅ Pass the figure to Streamlit



        # Explanation of the Big Five traits
        st.markdown("<h3 style='text-align: center; color: #4a4a4a;'>🧠 Understanding the Big Five Traits</h3>", unsafe_allow_html=True)

        trait_explanations = {
            "🌟 Openness": "🎨 Reflects creativity, curiosity, and openness to new experiences.",
            "📋 Conscientiousness": "✅ Indicates organization, responsibility, and reliability.",
            "🎤 Extraversion": "😃 Represents sociability, enthusiasm, and assertiveness.",
            "💙 Agreeableness": "🤝 Shows empathy, kindness, and cooperation.",
            "⚡ Neuroticism": "💭 Measures emotional stability and resilience to stress."
        }

        st.markdown("<div style='background-color: #f4f4f9; padding: 10px; border-radius: 10px;'>", unsafe_allow_html=True)

        for trait, description in trait_explanations.items():
            st.markdown(f"<p style='font-size: 18px;'><b>{trait}</b>: {description}</p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)



        
        os.remove(file_path)

# Run the app
if __name__ == "__main__":
    main()
