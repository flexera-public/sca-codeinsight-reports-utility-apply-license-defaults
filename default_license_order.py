'''
Copyright 2024 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Tue Mar 26 2024
File : default_license_order.py
'''

#######################################################################################################
#   licenseOrder is a dictionary where the license ID is they key which is used when comparing the
#       possible licenses for a given component to other possible licenses.  The order of preference
#       will be determined by where the license is entered into the list below.
#

licenseOrder = {}
# MIT
licenseOrder["7"] = "MIT License (MIT)"
# BSD
licenseOrder["389"] = "BSD 2-clause 'Simplified' License (BSD-2-Clause)"
licenseOrder["4"] = "BSD 3-clause 'New' or 'Revised' License (BSD-3-Clause)"
licenseOrder["692"] = "BSD 4-clause 'Original' or 'Old' License (BSD-4-Clause)"
# Apache
licenseOrder["388"] = "Apache License 2.0 (Apache-2.0)"
licenseOrder["5"] = "Apache License 1.1 (Apache-1.1)"
licenseOrder["20"] = "Apache License 1.0 (Apache-1.0)"
# GNU Library General Public License (LGPL
licenseOrder["1"] = "GNU Lesser General Public License v2.1 only (LGPL-2.1-only)"
licenseOrder["704"] = "GNU Lesser General Public License v2.1 or later (LGPL-2.1-or-later)"
licenseOrder["216"] = "GNU Lesser General Public License v3.0 only (LGPL-3.0-only)"
licenseOrder["705"] = "GNU Lesser General Public License v3.0 or later (LGPL-3.0-or-later)"
licenseOrder["199"] = "GNU Library General Public License v2 only (LGPL-2.0-only)"
licenseOrder["706"] = "GNU Library General Public License v2 or later (LGPL-2.0-or-later)"
# GNU General Public License v2.0 w/Classpath exception
licenseOrder["669"] = "GNU General Public License v2.0 w/Classpath exception (GPL-2.0-with-classpath-exception)"
# Mozilla Public License (MPL)
licenseOrder["1201"] = "Mozilla Public License 2.0 (MPL-2.0)"
licenseOrder["11"] = "Mozilla Public License 1.1 (MPL-1.1)"
licenseOrder["13"] = "Mozilla Public License 1.0 (MPL-1.0)"
# Common Development and Distribution License (CDDL)
licenseOrder["670"] = "Common Development and Distribution License 1.1 (CDDL-1.1)"
licenseOrder["48"] = "Common Development and Distribution License 1.0 (CDDL-1.0)"
# Eclipse Public License (EPL)
licenseOrder["1911"] = "Eclipse Public License 2.0 (EPL-2.0)"
licenseOrder["46"] = "Eclipse Public License 1.0 (EPL-1.0)"