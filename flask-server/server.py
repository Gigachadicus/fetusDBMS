from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tiger'
app.config['MYSQL_DB'] = 'testing'

mysql = MySQL(app)

@app.route("/results", methods=['POST'])
def results():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        cursor = mysql.connection.cursor()
        if query.strip().lower().startswith(('select', 'insert', 'update', 'delete')):
            cursor.execute(query)
            if query.strip().lower().startswith('select'):
                results = cursor.fetchall()
                return jsonify(results)
            mysql.connection.commit()
            return jsonify({"message": "Query executed successfully"})
        else:
            return jsonify({"error": "Invalid query type. Only SELECT, INSERT, UPDATE, and DELETE are allowed."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


@app.route("/tables", methods=["POST"])
def tables():
    try:
        res = dict()
        cursor = mysql.connection.cursor()
        cursor.execute("SHOW TABLES;")
        tableresults = cursor.fetchall()
        table_names = [table[0] for table in tableresults]

        for tablez in table_names:
            res[tablez] = []
            # Correct SQL quoting for table name
            cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tablez}';")
            temp = cursor.fetchall()
            cols = [i[0] for i in temp]
            res[tablez] = cols
        return jsonify(res)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()




@app.route("/generate_report", methods=['POST'])
def generate_report():
    return jsonify({"message": "Report generated successfully!"})
    # sales_data = {
    #     'total_sales': 15000,
    #     'best_sellers': [
    #         {'title': 'Book A', 'author': 'Author A', 'sold': 500},
    #         {'title': 'Book B', 'author': 'Author B', 'sold': 300},
    #     ]
    # }

    # inventory_data = {
    #     'total_books': 1200,
    #     'low_stock_books': 50,
    # }

    # customer_data = {
    #     'total_customers': 300,
    # }

    # report_filename = "bookstore_report.pdf"
    # c = canvas.Canvas(report_filename, pagesize=letter)
    # width, height = letter

    # # Title Page
    # c.setFont("Helvetica-Bold", 24)
    # c.drawString(100, height - 100, "Bookstore Management Analysis Report")
    # c.setFont("Helvetica", 12)
    # c.drawString(100, height - 130, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    # c.drawString(100, height - 150, "Prepared by: [Your Name]")
    # c.showPage()

    # # Executive Summary
    # c.setFont("Helvetica-Bold", 18)
    # c.drawString(100, height - 100, "Executive Summary")
    # c.setFont("Helvetica", 12)
    # c.drawString(100, height - 130, "This report provides an overview of sales, inventory, and customer analysis.")

    # # Sales Overview
    # c.setFont("Helvetica-Bold", 18)
    # c.drawString(100, height - 180, "Sales Overview")
    # c.setFont("Helvetica", 12)
    # c.drawString(100, height - 210, f"Total Sales: ${sales_data['total_sales']}")
    # c.drawString(100, height - 230, "Best-Selling Books:")
    
    # y_position = height - 250
    # for book in sales_data['best_sellers']:
    #     c.drawString(120, y_position, f"- {book['title']} by {book['author']} (Sold: {book['sold']})")
    #     y_position -= 20

    # # Inventory Status
    # c.setFont("Helvetica-Bold", 18)
    # c.drawString(100, y_position - 20, "Inventory Status")
    # c.setFont("Helvetica", 12)
    # c.drawString(100, y_position - 40, f"Total Books in Stock: {inventory_data['total_books']}")
    # c.drawString(100, y_position - 60, f"Low Stock Books: {inventory_data['low_stock_books']}")
    
    # # Customer Analysis
    # c.setFont("Helvetica-Bold", 18)
    # c.drawString(100, y_position - 80, "Customer Analysis")
    # c.setFont("Helvetica", 12)
    # c.drawString(100, y_position - 100, f"Total Customers: {customer_data['total_customers']}")

    # # Conclusion
    # c.setFont("Helvetica-Bold", 18)
    # c.drawString(100, y_position - 120, "Conclusion and Recommendations")
    # c.setFont("Helvetica", 12)
    # c.drawString(100, y_position - 140, "Consider increasing stock for best-selling books and analyze customer feedback.")

    # c.save()

    # return jsonify({"message": "Report generated successfully!", "filename": report_filename})

if __name__ == "__main__":
    app.run(debug=True)
