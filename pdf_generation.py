from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os
import csv
'''
#variables
x = 50
csv_file_path = "payments.csv"
#not using csv file because unsure whether it is center specific or just skool4kids, 
# setting them as varibles first

center_logo = 'testing_assets/Skool4Kidz-logo.png'
center_name = 'SKOOL4KIDZ PTE LTD'
center_address = "BLK 24 Marsiling Drive"
center_postal_code = "730024"
center_phone_number = "6368 9244"
center_fax_number = "6368 9243"
center_email = "marsilingcc@skool4kidz.com.sg"
center_url = "www.skool4kidz.com.sg"
'''
# Function to create a PDF receipt

def generate_pdf(entry, filename):

    x = 50
    csv_file_path = "payments.csv"

    center_logo = 'testing_assets/Skool4Kidz-logo.png'
    center_name = 'SKOOL4KIDZ PTE LTD'
    center_address = "BLK 24 Marsiling Drive"
    center_postal_code = "730024"
    center_phone_number = "6368 9244"
    center_fax_number = "6368 9243"
    center_email = "marsilingcc@skool4kidz.com.sg"
    center_url = "www.skool4kidz.com.sg"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Title

    y_position_client = 545 
    y_position = 0
    center_yposition = height - 50

    y_position_invoice = 600
    
    #c.setFont("Helvetica", 10)
    #C:\pdf_generation_component\testing_assets\Skool4Kidz-logo.png
    c.drawImage(center_logo, 50 , 700, width=180, height=90)
    

    c.setFont("Helvetica", 10)

    # Center Details
    center_info = [
    (center_name, 685),
    (center_address, 670),
    (f"SINGAPORE {center_postal_code}", 655),
    (f"Tel: {center_phone_number}", 640),
    (f"Fax: {center_fax_number}", 625),
    (center_email, 610),
    (center_url, 595)
    ]

    for text, y2_position in center_info:
        c.drawString(50, y2_position, text)


    #Client/Customer Details
    c.drawString(50, y_position_client + 15, "To:")
    c.drawString(50, y_position_client, f"Student: {entry['Student_Name']}")
    y_position_client -= 15
    c.drawString(50, y_position_client, f"Parent/ Guardian: {entry['Parent_Name']}")
    y_position_client -= 15
    c.drawString(50, y_position_client, f"Address: {entry['Address']}")
    y_position_client -= 15
    c.drawString(50, y_position_client, f"SNGAPORE: {entry['Postal_Code']}")
    y_position_client -= 15

    #Invice Details 
    c.setFont("Helvetica", 15)
    c.drawCentredString(295, y_position_invoice,"TAX INVOICE" )
    c.setFont("Helvetica", 12)
    c.drawCentredString(335, y_position_invoice - 40 ,f"Invoice No: {entry['Invoice_No']}")


   
    #making a table
    
    #drawing an image
    c.drawImage("testing_assets/qr_code_testing.jpg", 400, 650, width=150, height=150)
    
    # Assume 'c' is your canvas and 'entry' is a dictionary with 'Amount' as a key



    x = 50                  # Left margin
    y = height - 380       # Starting Y position from top
       # Width of each cell

    data = [
        ['DESCRIPTION', 'Amount', 'GST', 'SUB TOTAL'],
        [f"{entry['Description']}", f"{float(entry['Amount']):.2f}", f"{float(entry['GST'])}", f"{float(entry['Total_Amount']):.2f}"],
        ["Total Payable (S$)", f"{float(entry['Amount']):.2f}", f"{float(entry['GST'])}", f"{float(entry['Total_Amount']):.2f}"],
    ]

        # Predefine the heights row-wise (taller middle row)
    row_heights = [40, 260, 40]
    column_widths = [200, 100, 100, 100]

    for row in range(len(data)):
        row_height = row_heights[row]
        cell_y = y - sum(row_heights[:row])  # Adjust Y based on previous rows

        cell_x = x  # Reset x at the beginning of each row

        for col in range(len(data[row])):
            col_width = column_widths[col]

            if row == 0:
                c.setFillColor(colors.lightblue)
            elif row == 1:
                c.setFillColor(colors.whitesmoke)
            else:
                c.setFillColor(colors.lightgrey)

            
            c.rect(cell_x, cell_y - row_height, col_width, row_height, fill=1, stroke=1)

            # Set text color back to black (optional)
            c.setFillColor(colors.black)
            
            # Draw the cell border
            #c.rect(cell_x, cell_y - row_height, col_width, row_height)

            # Position text vertically 20 points from top of cell
            text_y = cell_y - 20

            if row == 0:
                # Centered text for header
                center_x = cell_x + col_width / 2
                c.drawCentredString(center_x, text_y, str(data[row][col]))
            else:
                # Left-aligned for other rows
                c.drawString(cell_x + 5, text_y, str(data[row][col]))

            # Move to the next column's x-position
            cell_x += col_width

    #Second Table for Billing Information
    
    x_billing = 280
    y_billing = 550



    row_heights_billing = [30,30]
    column_widths_billing = [100,100,70]

    billing_data = [
        ["Billing Date","Due Date","Amount"],
        [f"{entry['Billing_Date']}",f"{entry['Due_Date']}",f"{entry['Amount']}"]
    ]

    for row in range(len(billing_data)):
        row_height_billing = row_heights_billing[row]
        cell_y = y_billing - sum(row_heights_billing[:row])
        cell_x = x_billing

        for col in range(len(billing_data[row])):
            column_width_billing = column_widths_billing[col]

            # Background color
            if row == 0:
                c.setFillColor(colors.lightblue)
            else:
                c.setFillColor(colors.whitesmoke)

            # Draw cell
            c.rect(cell_x, cell_y - row_height_billing, column_width_billing, row_height_billing, fill=1, stroke=1)

            # Text color
            c.setFillColor(colors.black)

            # Text position
            text_y = cell_y - 20

            if row == 0:
                center_x = cell_x + column_width_billing / 2
                c.drawCentredString(center_x, text_y, str(billing_data[row][col]))
            else:
                c.drawString(cell_x + 5, text_y, str(billing_data[row][col]))

            # Move to next column
            cell_x += column_width_billing

    #Remarks Section
    c.setFont("Helvetica", 12)
    c.drawString(50, 100, "Remarks:")

    c.setFont("Helvetica", 10)
    c.drawString(50, 85, f"{entry['Remarks']}")

    c.save()







def generate_all_invoices_from_csv(csv_file_path, output_dir="Bill_Payments"):
    csv_file_path = "payments.csv"
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print("Directory has been created:", output_dir)

    # Read the CSV file and generate PDFs
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filename = os.path.join(output_dir, f"{row['Invoice_No']}_invoice.pdf")
            generate_pdf(row, filename)  # Make sure this function is defined elsewhere
            print("Generating Payments")
            print(f"Generated: {filename}")
csv_file_path = "payments.csv"
generate_all_invoices_from_csv(csv_file_path)



'''
# Create output directory
output_dir = "Bill_Payments"
os.makedirs(output_dir, exist_ok=True)
print("directory has been created")

# Read the CSV file and generate PDFs
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        filename = os.path.join(output_dir, f"{row['Invoice_No']}_invoice.pdf")
        generate_pdf(row, filename)
        print("Generating Payments")
        print(f"Generated: {filename}")'''