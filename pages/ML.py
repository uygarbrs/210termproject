import streamlit as st
import backend_league as bl

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="ML")

st.title("Machine Learning")

ml_container = st.container(border=True)

# accuracy
ml_container.subheader("Test Accurracy")
ml_container.write(bl.accuracy)
ml_container.divider()

# classification result
ml_container.subheader("Classification Report Result")

columns = ml_container.columns(4)
for label in bl.classification_report_result.keys():
    metrics = bl.classification_report_result[label]

    with columns[0]:
        st.markdown(f"**Class {label}**",
                    unsafe_allow_html=True)
    if type(metrics) == dict:
        with columns[1]:
            st.write(f"Precision: {metrics['precision']:.2f}")
        with columns[2]:
            st.write(f"Recall: {metrics['recall']:.2f}")
        with columns[3]:
            st.write(f"F1-score: {metrics['f1-score']:.2f}")
    else:
        with columns[1]:
            st.write("none")
        with columns[2]:
            st.write("none")
        with columns[3]:
            st.write(f"F1-score: {metrics:.2f}")

expander = ml_container.expander("See explanation")
explanation = """
This classification report provides information for two classes (0 and 1):

Precision: The ability of the classifier not to label as positive a sample that is negative.

Recall: The ability of the classifier to find all the positive samples.

F1-score: The weighted average of precision and recall.

Support: The number of actual occurrences of the class in the specified dataset.

"""
expander.write(explanation)

# feature importance
st.header("Feature Importances", divider="orange")

st.image("feature_importances.png")

feature_expander = st.expander("See the explanation for the chart")
feature_explanation = """
The chart above shows the importance ranking of the features (columns) 
that affect the game result.
"""
feature_expander.write(feature_explanation)
feature_expander.info("According to the chart, 'k-a' (sum of kill and assist) has the most "
                      "influence on the result.")

# prediction vs actual values
st.header("Prediction", divider="orange")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Predicted Values:")
    st.write(bl.y_pred)

with col2:
    st.subheader("Test Values (Actual Values):")
    st.write(bl.y_test.values)
st.info("As observed, prediction is only wrong for one value.")

# confusion matrix
st.header("Confusion Matrix", divider="orange")

st.image("confusion_matrix.png")

confusion_expander = st.expander("See the explanation for the chart")
confusion_explanation = """
The chart above is a better demonstration of how accurate the prediction is.

For instance, on the left side of the heatmap there are 10 values predicted for game result
as lose. 9 out of 10 instances were predicted correctly. A similar interpretation can be made
for the predictions for win result. All instances of wins are predicted correctly (13 out of 13).
"""
confusion_expander.write(confusion_explanation)