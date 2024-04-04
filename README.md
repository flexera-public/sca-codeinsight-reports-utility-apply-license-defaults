# Code Insight Apply License Defaults Utility

The `sca-codeinsight-reports-utility-apply-license-defaults` repository is a project utility that can be installed within the Code Insight custom report framework.

The purpose of this utility is to assign licenses to inventory items that do not currently have one selected.   The script will compare possible licenses to a list of licenses defined within [default_license_order.py](default_license_order.py) where the license will be used in the order they are entered into the list.

The script will cycle through each inventory item and if there is no license selected it will start at the top of the license list and compare to the list of possible licenses for the component.  If there is a match the license will be selected, the inventory item name will change to reflect the new license and the audit notes will be updated to show these changes.   These items will also be captured for the report artifact.

If there is no match for a priorities license to the list of possible license no action will be taken but this item will be captured for the report artifact.

Once completed an html document is created and summarizes the actions taken and show the items that were changed and which ones were not.


This repository utilizes the following via CDN for the creation of the report artifacts.
- [Bootstrap](https://getbootstrap.com/)
- [DataTables](https://datatables.net/)

## Prerequisites

 **Code Insight Release Requirements**
  
|Repository Tag|Minimum Code Insight Release  |
|--|--|
|1.0.x |2024R1  |

**Repository Cloning**

This repository should be cloned directly into the **$CODEINSIGHT_INSTALLDIR/custom_report_scripts** directory. If no prior custom reports has been installed, this directory may need to be created prior to cloning.

**Submodule Repositories**

This repository contains two submodule repositories for code that is used across multiple projects.  There are two options for cloning this repository and ensuring that the required submodules are also installed.

Clone the report repository use the recursive option to automatically pull in the required submodules

	git clone --recursive

 Alternatively clone the report repository and then clone the submodules separately by entering the cloned directory and then pulling down the necessary submodules code via   

	git submodule init

	git submodule update

**Python Requirements**

The required python modules can be installed with the use of the [requirements.txt](requirements.txt) file which can be loaded via.

    pip install -r requirements.txt    

## Configuration and Report Registration
 
For registration purposes the file **server_properties.json** should be created and located in the **$CODEINSIGHT_INSTALLDIR/custom_report_scripts/** directory.  This file contains a json with information required to register the report within Code Insight as shown  here:

>     {
>         "core.server.url": "http://localhost:8888" ,
>         "core.server.token" : "Admin authorization token from Code Insight"
>     }

The value for core.server.url is also used within [create_report.py](create_report.py) for any project or inventory based links back to the Code Insight server within a generated report.

If the common **server_properties.json** files is not used then the information the the following files will need to be updated:

[registration.py](registration.py)  -  Update the **baseURL** and **adminAuthToken** values. These settings allow the report itself to be registered on the Code Insight server.

[create_report.py](create_report.py)  -  Update the **baseURL** value. This URL is used for links within the reports.

Report option default values can also be specified in [registration_config.json](registration_config.json).

### Registering the Report

Prior to being able to call the script directly from within Code Insight it must be registered. The [registration.py](registration.py) file can be used to directly register the report once the contents of this repository have been copied into the custom_report_script folder at the base Code Insight installation directory.

To register this report:

    python registration.py -reg

To unregister this report:

    python registration.py -unreg

To update this report configuration:

    python registration.py -update

## Usage

This utility is executed directly from within Revenera's Code Insight product. From the project reports tab of each Code Insight project it is possible to *execute* the **Apply License Defaults Utility** via the Custom Report Framework.  

The following report options can be set once the report generation has been initiated:

- Including child projects (True/False) - Determine if child project data will be included or not.

The Code Insight Custom Report Framework will provide the following to the custom report when initiated:

- Project ID
- Report ID
- Authorization Token
- Report options

For this example report these four items are passed on to a batch or sh file which will in turn execute a python script. This script will then:

- Collect data for the report via REST API using the Project ID and Authorization Token
- Take this collected data and generated an html document with details about the project inventory
	- The *"viewable"* file   
 - Create a zip file of this html document
	  - The *"downloadable"* file
- Create a zip file with the viewable file and the downloadable file
- Upload this combined zip file to Code Insight via REST API
- Delete the report artifacts that were created as the script ran

  

## License

[MIT](LICENSE.TXT)