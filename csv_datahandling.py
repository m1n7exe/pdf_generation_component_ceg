import csv



def generate_invoice_id(filename='payments.csv'):
    try:
        # Try opening the CSV file for reading
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            # If the file is empty, start with the default 'INV1000'
            if len(rows) == 0:
                return 'INV1000'
            
            # Otherwise, get the last invoice number from the first column (Invoice_No)
            last_id = rows[-1][0]  # First column contains the invoice number
            # Remove 'INV' and convert to integer, then increment
            invoice_no = int(last_id[3:]) + 1  # Skip 'INV' and increment the number
            # Format the ID with leading zeros and return it
            return f"INV{invoice_no:04d}"

    except FileNotFoundError:
        # If the file doesn't exist, return default invoice ID 'INV1000'
        return 'INV1000'

def save_to_csv(data, filename='payments.csv'):
    """Save the form data into a CSV file."""
    headers = ['Invoice_No', 'Student_Id', 'Student_Name', 'Parent_Name', 'Address', 'Postal_Code', 'UEN', 'Billing_Date', 'Due_Date', 'Amount', 'GST', 'Total_Amount', 'Description', 'Payment_Scheme', 'Remarks']

    try:
        # Open the file in append mode
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Check if the file is empty and write headers if necessary
            file_empty = file.tell() == 0
            if file_empty:
                writer.writerow(headers)  # Write header row
            
            # Write the submitted data (invoice data) to the CSV
            writer.writerow(data)
        print("Data saved successfully!")
    
    except Exception as e:
        print(f"Error saving data: {e}")
