#!/usr/bin/env python

########################################################################################################################
# check_mk_to_securecrt_export_helper - Export Check_MK hosts to SecureCRT Session Manager
# Version 0.1 - Written by Maximilian Thoma 2020
# Checkout https://github.com/lanbugs/check_mk_to_securecrt_export or https://lanbugs.de for updates.
#
# Released under GPL Version 2 - see LICENSE file for details
########################################################################################################################

import urllib.parse
import urllib.request
import json
import ssl

########################################################################################################################
# Settings

# User to interact with check_mk, user need automation secret!
user = "securecrt"

# Automation secret
secret = "OYPCCOJCCMDPQSCLYFOI"

# URL to check_mk instance with ? at the end
url = "https://checkmk.company.local/core/check_mk/view.py?"

# View which shows prefiltered the hosts you want to create sessions in check_mk
# Only tree columns are allowed in the view:
# hostname,ip,wato_folder_abs
# See details on https://github.com/lanbugs/check_mk_to_securecrt_export or https://lanbugs.de
# You can test it manually if you browse the url in an browser.
# e.g. https://checkmk.company.corp/central_mon/check_mk/view.py?view_name=allhosts_securecrt&_username=securecrt&_secret=OYPCCOJCCMDPQSCLYFOI&output_format=json
# You should see an json output with the 3 columns.
view_name = "allhosts_securecrt"


########################################################################################################################
# Code - do not change anything below

query_params = None

if not query_params:
    query_params = {}

query_params.update({
    'view_name': view_name,
    'output_format': "json",
    '_username': user,
    '_secret': secret
})

query_string = urllib.parse.urlencode(query_params)

url += query_string

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

response = urllib.request.urlopen(url, context=ctx)
filex = json.loads(response.read().decode())

for l in filex:
    print("{},{},{}".format(l[0], l[1], l[2]))
