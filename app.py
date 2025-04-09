from flask import Flask, request, render_template, redirect, url_for
from pdf_generation import generate_pdf, generate_all_invoices_from_csv
from csv_datahandling import generate_invoice_id, save_to_csv
import csv
import os

csv_filepath = "payments.csv"
csv_file_path = "payments.csv"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_invoice_details', methods=['POST'])
def handle_form_submission():
    print("Form submitted.")
    
    student_id = request.form.get('Student_Id')
    student_name = request.form.get('Student_Name')
    parent_name = request.form.get('Parent_Name')
    address = request.form.get('Address')
    postal_code = request.form.get('Postal_Code')
    billing_date = request.form.get('Billing_Date')
    due_date = request.form.get('Due_Date')
    description = request.form.get('Description')
    amount = request.form.get('Amount')
    gst = request.form.get('GST')
    payment_mode = request.form.get('paymentMode')
    remarks = request.form.get('Remarks')
    
    #sample data and varaibles before working ore on the functions
    #for the rest of the data
    invoice_id = "INV9999"
    uen = "12345678"
    total_amount = float(amount) + float(gst)  # You can convert strings to float for calculation



    # Print all the form data to check if anything is missing
    print("Form Data:")
    print(f"Student ID: {student_id}, Student Name: {student_name}, Parent Name: {parent_name}")
    
    invoice_data = [
        invoice_id, 
        student_id,
        student_name,
        parent_name,
        address,
        postal_code,
        uen,
        total_amount,
        billing_date,
        due_date,
        amount,
        gst,
        description,
        payment_mode,
        remarks]
    
    print("Invoice Data:")
    print(invoice_data)
    
    # Save to CSV
    save_to_csv(invoice_data)
    #this part is not working properly, it is not generating invoice 9999
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        last_entry = reader[-1]

        # ⚠️ Optional: print the last entry to debug
        print("Last entry to generate PDF:", last_entry)

        filename = os.path.join("Bill_Payments", f"{last_entry['Invoice_No']}_invoice.pdf")
        os.makedirs("Bill_Payments", exist_ok=True)
        generate_pdf(last_entry, filename)

    return redirect(url_for('payment'))


@app.route('/payment')
def payment():
    return render_template("payment.html")


if __name__ == '__main__':
    app.run(debug=True)