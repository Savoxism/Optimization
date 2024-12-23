import streamlit as st
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import torch

# Define model and tokenizer paths
fine_tuned_model_dir = "Savoxism/distilbert_sentiment_analysis_final"
tokenizer_dir = fine_tuned_model_dir

@st.cache_resource  
def load_model_and_tokenizer(model_path, tokenizer_path):
    try:
        model = DistilBertForSequenceClassification.from_pretrained(model_path)
        tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_path)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        model.eval()
        st.success("Model and tokenizer loaded successfully!")
        return model, tokenizer, device # Return the model, tokenizer and device
    except Exception as e:
        st.error(f"Error loading model or tokenizer: {e}")
        st.stop()
        return None, None, None 

model, tokenizer, device = load_model_and_tokenizer(fine_tuned_model_dir, tokenizer_dir)

if model is None or tokenizer is None:
    st.stop()

def classify_review(review, model, tokenizer, device, max_length=64):
    inputs = tokenizer(
        review,
        padding="max_length",
        truncation=True,
        max_length=max_length,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(logits, dim=-1).item()

    label_mapping = {0: "Positive", 1: "Negative", 2: "Neutral"}
    sentiment = label_mapping[prediction]
    return sentiment

st.title("Sentiment Analysis App")
st.subheader("Enter a review and analyze its sentiment:")

review_text = st.text_area("Review", key="review_input") 

if st.button("Evaluate"):
    if review_text:
        predicted_sentiment = classify_review(review_text, model, tokenizer, device)
        st.success(f"Review: {review_text}")
        st.write(f"Predicted Sentiment: {predicted_sentiment}")
    else:
        st.warning("Please enter a review to analyze.")