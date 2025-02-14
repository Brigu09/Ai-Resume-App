from analysis import extract_text_from_pdf, personality_prediction_traits

text = extract_text_from_pdf("Test_Data.pdf")
scores = personality_prediction_traits(text)
print(scores)