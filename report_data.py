'''
Copyright 2024 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Wed Mar 27 2024
File : report_data.py
'''
import logging
import common.project_heirarchy
import common.api.project.get_project_inventory
import common.api.component.component_version
import common.api.license.license_lookup
import common.api.inventory.update_inventory
import default_license_order


logger = logging.getLogger(__name__)

#-------------------------------------------------------------------#
def gather_data_for_report(baseURL, authToken, reportData):
    logger.info("Entering gather_data_for_report")

    licenseDetails = {}  # Dict with license ID as key and SPDX ID as value
    updateDetails = {}   # Dict to store details as to what was updated

    projectID = reportData["primaryProjectID"]
    reportOptions = reportData["reportOptions"]

    # Parse report options
    includeChildProjects = False  # Hardcode since child projects not supported

    projectList = common.project_heirarchy.create_project_heirarchy(baseURL, authToken, projectID, includeChildProjects)
    topLevelProjectName = projectList[0]["projectName"]
    # Get the list of parent/child projects start at the base project
    projectHierarchy = common.api.project.get_child_projects.get_child_projects_recursively(baseURL, projectID, authToken)

    reportData["topLevelProjectName"] = topLevelProjectName
    reportData["projectID"] = projectID
    reportData["projectList"] =projectList
    reportData["projectHierarchy"] = projectHierarchy

    # Collect details for each project
    for project in projectList:

        updatedInventoryItems = []
        projectID = project["projectID"]
        projectName = project["projectName"]
        projectLink = project["projectLink"] 

        APIOPTIONS = "&includeFiles=false&skipVulnerabilities=true"
        projectInventoryDetails = common.api.project.get_project_inventory.get_project_inventory_details_with_options(baseURL, projectID, authToken, APIOPTIONS)

        if "error" in projectInventoryDetails:
                reportData["error"] = projectInventoryDetails["error"]
                return reportData


        inventoryItems = projectInventoryDetails["inventoryItems"] 

        numInventoryItems = len(inventoryItems)
        unchangedInventory = 0

        for inventoryItem in inventoryItems:
            inventoryItemName = inventoryItem["name"]
            inventoryId = inventoryItem["id"]
            componentId = inventoryItem["componentId"]
            componentVersionId = inventoryItem["componentVersionId"]
            selectedLicenseId = str(inventoryItem["selectedLicenseId"])
            auditNotes = inventoryItem["auditNotes"]

            inventoryLink = baseURL + "/codeinsight/FNCI#myprojectdetails/?id=" + str(projectID) + "&tab=projectInventory&pinv=" + str(inventoryId)

            # Is there a license selected for this inventory item?
            if selectedLicenseId == "-1":

                # Get a list of the possible license for the specific version of component

                componentVersionDetails = common.api.component.component_version.get_component_versions_details(baseURL, authToken, componentVersionId)

                if "error" in componentVersionDetails:
                     reportData["error"] = componentVersionDetails["error"]
                     return reportData
                               
                # Create list of possible license IDs
                possibleLicenseIds = []
                for license in componentVersionDetails["licenses"]:
                    possibleLicenseIds.append(str(license["id"]))

                # See if each license in the default license order is in the possible license list
                # If yes then change the inventory item to have the license from top to bottom in 
                # order of preference
                match = False
                for licenseID in default_license_order.licenseOrder:

                    if componentVersionId == "N/A":
                        # There is no version specified so it cannot be processed
                        match=False
                        break

                    if licenseID in possibleLicenseIds:
                        # This is the preferred license so we need the SPDX license ID
                        # to update the inventory item's name
                        if licenseID in licenseDetails:
                            shortName = licenseDetails[licenseID]
                        else:
                            licenseDetail = common.api.license.license_lookup.get_license_details(baseURL, licenseID, authToken)
                            shortName = licenseDetail["shortName"]
                            licenseDetails[licenseID] = shortName

                        # Strip off the original license name by the last ()
                        newInventoryItemName = inventoryItemName.rsplit("(", 1)[0]
                        newInventoryItemName += "(%s)" %shortName

                        # If there are already auditnote append an update
                        if auditNotes != "":
                            auditNotes += "<p>++++++++<p>"
                        
                        auditNotes += "Selected license and inventory item name updated via sca-codeinsight-reports-apply-license-defaults-utility"

                        updateBody =  '''
                            {
                            "name" : "%s",

                            "inventoryType": "COMPONENT",
                            "component": {
                                "id": "%s",
                                "versionId": "%s",
                                "licenseId": "%s"
                            },
                            "licenseId" : "%s",
                            "auditorReviewNotes": "%s"
                            }
                        ''' %(newInventoryItemName, componentId, componentVersionId, licenseID, licenseID, auditNotes)

                        logger.info("Updating inventory with ID %s")
                        logger.info("    Original Name: %s" %inventoryItemName)
                        logger.info("         New Name: %s" %newInventoryItemName)
                        response = common.api.inventory.update_inventory.update_inventory_item_details(inventoryId, updateBody, baseURL, authToken)

                        if "error" in response:
                            return response

                        details = {}
                        details["inventoryId"] = inventoryId
                        details["inventoryLink"] = inventoryLink
                        details["licenseId"] = licenseID
                        details["shortName"] = shortName
                        details["inventoryItemName"] = inventoryItemName
                        details["newInventoryItemName"] = newInventoryItemName
                        updatedInventoryItems.append(details)
                        match = True
                        break
                # There was not a license match found in the list of preferred licenses
                if not match:
                    details = {}
                    details["inventoryId"] = inventoryId
                    details["inventoryLink"] = inventoryLink
                    details["licenseId"] = ""
                    details["shortName"] = ""
                    details["inventoryItemName"] = inventoryItemName
                    details["newInventoryItemName"] = ""
                    updatedInventoryItems.append(details)
                    unchangedInventory +=1
            

        updateDetails[projectName] = {}
        updateDetails[projectName]["projectLink"] = projectLink
        updateDetails[projectName]["projectID"] = projectID
        updateDetails[projectName]["numInventoryItems"] = numInventoryItems
        updateDetails[projectName]["numInventoryItemsNotNeededChanges"] = numInventoryItems - len(updatedInventoryItems)
        updateDetails[projectName]["numInventoryChangesNeeded"] = len(updatedInventoryItems)
        updateDetails[projectName]["numChangedInventory"] = len(updatedInventoryItems) - unchangedInventory
        updateDetails[projectName]["numUnchangedInevntory"] = unchangedInventory
        updateDetails[projectName]["updatedInventoryItems"] = updatedInventoryItems

    reportData["updateDetails"] = updateDetails

    return reportData