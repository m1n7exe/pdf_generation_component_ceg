from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os
import csv

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

# Function to create a PDF receipt
def generate_pdf(entry, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Title

    y_position_client = 545 
    y_position = 0
    center_yposition = height - 50
    
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


    #Billing Information




    c.drawString(50, y_position, f"Invoice No: {entry['Invoice_No']}")
    y_position -= 15
    c.drawString(50, y_position, f"Student ID: {entry['Student_Id']}")
    y_position -= 15
    c.drawString(50, y_position, f"Student Name: {entry['Student_Name']}")
    y_position -= 15
    c.drawString(50, y_position, f"Parent Name: {entry['Parent_Name']}")
    y_position -= 15
    c.drawString(50, y_position, f"Address: {entry['Address']}")
    y_position -= 15
    c.drawString(50, y_position, f"UEN: {entry['UEN']}")
    y_position -= 15
    c.drawString(50, y_position, f"Billing Date: {entry['Billing_Date']}")
    y_position -= 15
    c.drawString(50, y_position, f"Due Date: {entry['Due_Date']}")
    y_position -= 15
    c.drawString(50, y_position, f"Amount: ${float(entry['Amount']):.2f}")
    y_position -= 15
    c.drawString(50, y_position, f"GST: ${float(entry['GST']):.2f}")
    y_position -= 15
    c.drawString(50, y_position, f"Total Amount: ${float(entry['Total_Amount']):.2f}")
    y_position -= 15
    c.drawString(50, y_position, f"Description: {entry['Description']}")
    y_position -= 15
    c.drawString(50, y_position, f"Remarks: {entry['Remarks']}")
    y_position -= 15

    #making a table
    
    #drawing an image
    c.drawImage("testing_assets/qr_code_testing.jpg", 450, 680, width=100, height=100)
    
    # Assume 'c' is your canvas and 'entry' is a dictionary with 'Amount' as a key



    x = 50                  # Left margin
    y = height - 380       # Starting Y position from top
    cell_width = 130        # Width of each cell

    data = [
        ['DESCRIPTION', 'AMOUNT', 'GST', 'SUB TOTAL'],
        [f"{entry['Description']}", f"{float(entry['Amount']):.2f}", f"{float(entry['GST'])}", f"{float(entry['Total_Amount']):.2f}"],
        ["Total Payable (S$)", f"{float(entry['Amount']):.2f}", f"{float(entry['GST'])}", f"{float(entry['Total_Amount']):.2f}"],
    ]

        # Predefine the heights row-wise (taller middle row)
    row_heights = [40, 200, 40]
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

    c.save()



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
        print(f"Generated: {filename}")
