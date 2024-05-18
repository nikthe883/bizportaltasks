import xml.etree.ElementTree as ET
import pandas as pd

class XMLParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def parse_large_xml(self):
        # Use iterparse to incrementally parse the XML file and track 'end' events for 'FullNotice' elements
        context = ET.iterparse(self.file_path, events=("end",))
        context = iter(context)
        event, root = next(context) 

        for event, elem in context:
            if event == "end" and elem.tag == "FullNotice":
                # Extract required fields
                publish_date = elem.findtext('PublishedDate')
                award_date = elem.findtext('CreatedDate')
                title = elem.findtext('Title')
                short_description = elem.findtext('Description')
                awarded_company = elem.findtext('.//Organisation/Name')
                awarded_company_address = elem.findtext('.//ContactDetails/Address1')
                awarded_value = elem.findtext('.//AwardDetail/Value')
                url = "https://www.contractsfinder.service.gov.uk/notice/" + elem.findtext('Id')

                # Collect data
                self.data.append([
                    publish_date, award_date, title, short_description, 
                    awarded_company, awarded_company_address, awarded_value, url
                ])
                
                
                root.clear()

    def save_to_excel(self, filename):
        df = pd.DataFrame(self.data, columns=[
            'Publish Date', 'Date of Award', 'Title', 'Short Description', 
            'Awarded Company', 'Awarded Company Address', 'Awarded Value', 'URL'
        ])
        df.to_excel(filename, index=False)

# Declarin file path and output file names
file_path = 'notices.xml'
output_file = 'awarded_contracts_uk.xlsx'

# Create an instance of the XMLParser class
parser = XMLParser(file_path)

# Parse the large XML file
parser.parse_large_xml()

# Save the extracted data to an Excel file
parser.save_to_excel(output_file)
