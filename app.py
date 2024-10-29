from flask import Flask, request, jsonify,render_template
import pandas as pd

app = Flask(__name__)

# Load data from the CSV file
def load_data_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    # Convert the DataFrame to a dictionary for easier access
    return df.set_index('Company').T.to_dict()

# Load data
data = load_data_from_csv('Year_to_year_report.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    
    user_input = request.form.get('question', '').lower()
    response = {}

    if "revenue growth" in user_input:
        company = extract_company(user_input)
        if company and company in data:
            response['answer'] = f"{company} Revenue Growth: {data[company]['Revenue Growth (%)']}%"
        else:
            response['answer'] = "I'm sorry, I don't have that information."

    elif "net income growth" in user_input:
        company = extract_company(user_input)
        if company and company in data:
            response['answer'] = f"{company} Net Income Growth: {data[company]['Net Income Growth (%)']}%"
        else:
            response['answer'] = "I'm sorry, I don't have that information."

    else:
        response['answer'] = "I can answer questions about Revenue Growth and Net Income Growth for Apple, MSFT, and Tesla."

    return jsonify(response)

def extract_company(question):
    companies = data.keys()
    for company in companies:
        if company.lower() in question:
            return company
    return None

if __name__ == '__main__':
    app.run(debug=True)