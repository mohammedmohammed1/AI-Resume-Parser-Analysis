AI-Resume-Parser-Analysis
AI-powered Resume Prediction app using Streamlit and ML. Extracts resume text, predicts job roles, stores results in SQLite, and offers easy management of predictions. A simple yet effective tool for resume analysis and career insights
Perfect 

 📌 README.md

Resume Prediction App  

An AI-powered application that analyzes resumes, predicts job roles, and stores results in an SQLite database. Built with **Streamlit** and **scikit-learn**, this project provides a simple yet effective way to parse, analyze, and manage resumes.  

 🚀 Features
- Extracts text from resumes (PDF/DOCX).  
- Predicts job roles using Machine Learning.  
- Stores and manages predictions in SQLite.  
- User-friendly **Streamlit UI**.  
- Option to delete or manage past predictions.  

 🛠️ Tech Stack
- Python  
- Streamlit  
- scikit-learn 
- SQLite
- pandas, PyMuPDF, python-docx  

📂 Project Structure

Resume Prediction.ipynb   
predictor.py              
requirements.txt          
README.md                

⚡ Installation & Usage
1. Clone the repository  

   git clone https://github.com/yourusername/resume-prediction.git
   cd resume-prediction

2. Install dependencies

   pip install -r requirements.txt

3. Run the Streamlit app

   streamlit run predictor.py
  
📊 Example Workflow

1. Upload a resume (PDF/DOCX).
2. App extracts and processes text.
3. ML model predicts the most relevant job role.
4. Prediction is saved in SQLite and can be managed later.

📜 License

This project is licensed under the MIT License.

 🙌 Acknowledgements

* scikit-learn for ML models
* Streamlit for building an interactive app
* SQLite for lightweight database management

