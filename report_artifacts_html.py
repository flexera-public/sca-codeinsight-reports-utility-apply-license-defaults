'''
Copyright 2024 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Wed Mar 27 2024
File : report_artifacts_html.py
'''
import logging, os, base64
import _version

logger = logging.getLogger(__name__)

#------------------------------------------------------------------#
def generate_html_report(reportData):
    logger.info("    Entering generate_html_report")

    reportName = reportData["reportName"]   
    reportFileNameBase = reportData["reportFileNameBase"]
    reportTimeStamp =  reportData["reportTimeStamp"] 
    
    scriptDirectory = os.path.dirname(os.path.realpath(__file__))
    cssFile =  os.path.join(scriptDirectory, "common/branding/css/revenera_common.css")
    logoImageFile =  os.path.join(scriptDirectory, "common/branding/images/logo_reversed.svg")
    iconFile =  os.path.join(scriptDirectory, "common/branding/images/favicon-revenera.ico")

    #########################################################
    #  Encode the image files
    encodedLogoImage = encodeImage(logoImageFile)
    encodedfaviconImage = encodeImage(iconFile)

    htmlFile = reportFileNameBase + ".html"

    logger.debug("        htmlFile: %s" %htmlFile)

    #---------------------------------------------------------------------------------------------------
    # Create a simple HTML file to display
    #---------------------------------------------------------------------------------------------------
    try:
        html_ptr = open(htmlFile,"w")
    except:
        logger.error("Failed to open htmlfile %s:" %htmlFile)
        raise

    html_ptr.write("<html>\n") 
    html_ptr.write("    <head>\n")

    html_ptr.write("        <!-- Required meta tags --> \n")
    html_ptr.write("        <meta charset='utf-8'>  \n")
    html_ptr.write("        <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'> \n")

    html_ptr.write(''' 
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.6.2/css/bootstrap.css"> 
        <link rel="stylesheet" href="https://cdn.datatables.net/1.13.8/css/dataTables.bootstrap4.min.css">            
    ''')


    html_ptr.write("        <style>\n")

    # Add the contents of the css file to the head block
    try:
        f_ptr = open(cssFile)
        logger.debug("        Adding css file details")
        for line in f_ptr:
            html_ptr.write("            %s" %line)
        f_ptr.close()
    except:
        logger.error("Unable to open %s" %cssFile)
        print("Unable to open %s" %cssFile)

    # TODO Add to css file
    html_ptr.write(" .tr-notExactMatch { background-color: #F0F0F0;}\n")
    html_ptr.write(" .td-nomatch { color: #F80000;}\n")
    html_ptr.write(" .btn-comparison {  width:250px; background-color: #323E48; color: #FFFFFF;}\n")
    # To keep the filter button a different color after it was clicked
    html_ptr.write(".active {  background-color: #89EE46; color: #000000; outline-color: red;}")

    
    html_ptr.write("        </style>\n")  

    html_ptr.write("    	<link rel='icon' type='image/png' href='data:image/png;base64, {}'>\n".format(encodedfaviconImage.decode('utf-8')))
    html_ptr.write("        <title>%s</title>\n" %(reportName))
    html_ptr.write("    </head>\n") 

    html_ptr.write("<body>\n")
    html_ptr.write("<div class=\"container-fluid\">\n")

    #---------------------------------------------------------------------------------------------------
    # Report Header
    #---------------------------------------------------------------------------------------------------
    html_ptr.write("<!-- BEGIN HEADER -->\n")
    html_ptr.write("<div class='header'>\n")
    html_ptr.write("  <div class='logo'>\n")
    html_ptr.write("    <img src='data:image/svg+xml;base64,{}' style='height: 5%'>\n".format(encodedLogoImage.decode('utf-8')))
    html_ptr.write("  </div>\n")
    html_ptr.write("<div class='report-title'>%s</div>\n" %reportName)
    html_ptr.write("</div>\n")
    html_ptr.write("<!-- END HEADER -->\n")


    #---------------------------------------------------------------------------------------------------
    # Body of Report
    #---------------------------------------------------------------------------------------------------
    html_ptr.write("<!-- BEGIN BODY -->\n")  

    html_ptr.write("<center><h2>Inventory Change Summary</h2></center>")


    html_ptr.write("<table id='summaryData' class='table table-hover row-border table-sm' style='width:90%'>\n")    
    html_ptr.write("    <colgroup>\n")
    #html_ptr.write("        <col span=\"1\" style=\"width: 25%;\">\n")  # Project Name
    html_ptr.write("        <col span=\"1\" style=\"width: 15%;\">\n")  # Total Inventory Count
    html_ptr.write("        <col span=\"1\" style=\"width: 15%;\">\n")  # Inventory Not Requiring Changes
    html_ptr.write("        <col span=\"1\" style=\"width: 15%;\">\n")  # Inventory Requiring Changes
    html_ptr.write("        <col span=\"1\" style=\"width: 15%;\">\n")  # Inventory Changed
    html_ptr.write("        <col span=\"1\" style=\"width: 15%;\">\n")  # Inventory Unchanged
    html_ptr.write("    </colgroup>\n")

    html_ptr.write("    <thead>\n")
    html_ptr.write("       <tr>\n")
    #html_ptr.write("           <th class='text-left'>Project</th>\n") 
    html_ptr.write("           <th class='text-center'>Total Inventory Count</th>\n")
    html_ptr.write("           <th class='text-center'>Inventory Not Requiring Changes</th>\n")
    html_ptr.write("           <th class='text-center'>Inventory Requiring Changes</th>\n")
    html_ptr.write("           <th class='text-center'>Inventory Changed</th>\n")
    html_ptr.write("           <th class='text-center'>Inventory Unchanged</th>\n")
    html_ptr.write("       </tr>\n")
    html_ptr.write("    <thead>\n")

    html_ptr.write("    <tbody>\n")

    for projectName in reportData["updateDetails"]:
        updateDetails = reportData["updateDetails"][projectName]
        projectLink = updateDetails["projectLink"]
        numInventoryItems = updateDetails["numInventoryItems"]
        numInventoryItemsNotNeededChanges = updateDetails["numInventoryItemsNotNeededChanges"]
        numInventoryChangesNeeded = updateDetails["numInventoryChangesNeeded"]
        numChangedInventory = updateDetails["numChangedInventory"] 
        numUnchangedInevntory = updateDetails["numUnchangedInevntory"] 

        html_ptr.write("       <tr>\n")
        #html_ptr.write("          <td class='text-left'><a href='%s' target='_blank' > %s</a></td>\n" %(projectLink, projectName))
        html_ptr.write("          <td class='text-center'>%s</td>\n" %numInventoryItems)
        html_ptr.write("          <td class='text-center'>%s</td>\n" %numInventoryItemsNotNeededChanges)
        html_ptr.write("          <td class='text-center'>%s</td>\n" %numInventoryChangesNeeded)
        html_ptr.write("          <td class='text-center'>%s</td>\n" %numChangedInventory)
        html_ptr.write("          <td class='text-center'>%s</td>\n" %numUnchangedInevntory)
        html_ptr.write("       </tr>\n")

    html_ptr.write("    </tbody>\n")
    html_ptr.write("</table>\n")

    html_ptr.write("<p><hr><p>\n")

    html_ptr.write("<center><h2>Inventory Change Data</h2></center>")

    html_ptr.write("<table id='inventoryData' class='table table-hover row-border table-sm' style='width:90%'>\n")

    html_ptr.write("    <colgroup>\n")
    #html_ptr.write("        <col span=\"1\" style=\"width: 15%;\">\n")  # Project
    html_ptr.write("        <col span=\"1\" style=\"width: 35%;\">\n")  # New Name
    html_ptr.write("        <col span=\"1\" style=\"width: 15%;\">\n")  # License
    html_ptr.write("        <col span=\"1\" style=\"width: 35%;\">\n")  # Orig Name
    html_ptr.write("    </colgroup>\n")

    html_ptr.write("    <thead>\n")
    html_ptr.write("       <tr>\n")
    #html_ptr.write("           <th class='text-left'>Project</th>\n") 
    html_ptr.write("           <th class='text-left'>Original Inventory Name</th>\n")
    html_ptr.write("           <th class='text-left'>Selected License</th>\n")
    html_ptr.write("           <th class='text-left'>New Inventory Name</th>\n")
    html_ptr.write("       </tr>\n")
    html_ptr.write("    <thead>\n")

    html_ptr.write("    <tbody>\n")

    for projectName in reportData["updateDetails"]:
        updateDetails = reportData["updateDetails"][projectName]
        projectLink = updateDetails["projectLink"]
        updatedInventoryItems =  updateDetails["updatedInventoryItems"]

        for updatedInventoryItem in updatedInventoryItems:
            html_ptr.write("       <tr>\n")
            #html_ptr.write("          <td class='text-left'><a href='%s' target='_blank' > %s</a></td>\n" %(projectLink, projectName))
            # Hyperlink the orig name if a new was was not created
            if updatedInventoryItem["newInventoryItemName"] == "":
                html_ptr.write("          <td class='text-left'><a href='%s' target='_blank' > %s</a></td>\n" %(updatedInventoryItem["inventoryLink"], updatedInventoryItem["inventoryItemName"]))
            else:
                html_ptr.write("          <td class='text-left'>%s</td>\n" %updatedInventoryItem["inventoryItemName"])

            html_ptr.write("          <td class='text-left'>%s</td>\n" %updatedInventoryItem["shortName"])
            html_ptr.write("          <td class='text-left'><a href='%s' target='_blank' > %s</a></td>\n" %(updatedInventoryItem["inventoryLink"], updatedInventoryItem["newInventoryItemName"]))

            


            html_ptr.write("       </tr>\n")
    html_ptr.write("    <tbody>\n")        
    html_ptr.write("<table>\n")   

    html_ptr.write("<!-- END BODY -->\n")  

    #---------------------------------------------------------------------------------------------------
    # Report Footer
    #---------------------------------------------------------------------------------------------------
    html_ptr.write("<!-- BEGIN FOOTER -->\n")
    html_ptr.write("<div class='report-footer'>\n")
    html_ptr.write("  <div style='float:right'>Generated on %s</div>\n" %reportTimeStamp)
    html_ptr.write("<br>\n")
    html_ptr.write("  <div style='float:right'>Report Version: %s</div>\n" %_version.__version__)
    html_ptr.write("</div>\n")
    html_ptr.write("<!-- END FOOTER -->\n")  

    html_ptr.write("</div>\n")


    html_ptr.write('''

    <script src="https://code.jquery.com/jquery-3.7.1.slim.min.js" integrity="sha256-kmHvs0B+OpCW5GVHUNjv9rOmY0IvSIRcf7zGUDTDQM8=" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js" integrity="sha384-+sLIOodYLS7CIrQpBjl+C7nPvqq+FbNUBDunl/OZv93DB7Ln/533i8e/mZXLi/P+" crossorigin="anonymous"></script>   
    <script src="https://cdn.datatables.net/1.13.8/js/jquery.dataTables.min.js"></script>  
    <script src="https://cdn.datatables.net/1.13.8/js/dataTables.bootstrap4.min.js"></script> 


    ''')

    html_ptr.write("<script>\n")

    html_ptr.write('''
            var table = $('#inventoryData').DataTable(
                {"lengthMenu": [ [25, 50, 100, -1], [25, 50, 100, "All"] ],}
            );''')

    html_ptr.write("</script>\n")



    html_ptr.write("</body>\n") 
    html_ptr.write("</html>\n") 
    html_ptr.close() 

    logger.info("    Exiting generate_html_report")
    return htmlFile


####################################################################
def encodeImage(imageFile):

    #############################################
    # Create base64 variable for branding image
    try:
        with open(imageFile,"rb") as image:
            encodedImage = base64.b64encode(image.read())
            return encodedImage
    except:
        logger.error("Unable to open %s" %imageFile)
        raise