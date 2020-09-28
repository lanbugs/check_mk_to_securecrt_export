# $language = "Python"
# $interface = "1.0"

########################################################################################################################
# check_mk_to_securecrt_export - Export Check_MK hosts to SecureCRT Session Manager
# Version 0.1 - Written by Maximilian Thoma 2020
# Checkout https://github.com/lanbugs/check_mk_to_securecrt_export or https://lanbugs.de for updates.
#
# Released under GPL Version 2 - see LICENSE file for details
########################################################################################################################

import os
from subprocess import check_output

out = check_output(['%s\\dist\\check_mk_to_securecrt_export_helper\\check_mk_to_securecrt_export_helper.exe' % os.path.dirname(os.path.realpath(__file__))])

line = 0

# Check if username argument is present
if crt.Arguments.Count != 0:
    username = crt.Arguments[0]

# Use username from default settings
else:
    objConfig = crt.OpenSessionConfiguration("Default")
    username = objConfig.GetOption("Username")

# Work on every host in response
for l in out.splitlines():
    # ignore line null, header of csv output
    if line == 0:
        line += 1
        continue

    # create session
    else:
        hostname, ip, path = l.split(",")

        path = path.replace("Main directory", "_Check_MK_Imports").replace(" ", "")

        strDefaultProtocol = "SSH2"

        strSessionPath = "%s/%s" % (path, hostname)
        strPort = "22"
        strProtocol = "SSH2"
        strHostName = ip
        strUserName = username
        strEmulation = "xterm"
        strFolder = ""
        strDescription = ""
        strLogonScript = ""
        strSessionName = hostname

        objConfig = crt.OpenSessionConfiguration("Default")

        objConfig.SetOption("Protocol Name", strProtocol)

        objConfig.Save(strSessionPath)

        objConfig = crt.OpenSessionConfiguration(strSessionPath)

        vDescription = strDescription.split("\r")
        objConfig.SetOption("Description", vDescription)
        objConfig.SetOption("Emulation", strEmulation)

        if strLogonScript != "":
            objConfig.SetOption("Script Filename V2", strLogonScript)
            objConfig.SetOption("Use Script File", True)

        if strDescription != "":
            vDescription = strDescription.split("\r")
            objConfig.SetOption("Description", vDescription)

        if strHostName != "":
            objConfig.SetOption("Hostname", strHostName)

        if strUserName != "":
            objConfig.SetOption("Username", strUserName)

        if strProtocol.upper() == "SSH2":
            if strPort == "":
                strPort = 22
            objConfig.SetOption("[SSH2] Port", int(strPort))

        objConfig.SetOption("ANSI Color", True)
        objConfig.SetOption("Color Scheme", "Solarized Darcula") # Requires 8.3 or newer
        objConfig.SetOption("Color Scheme Overrides Ansi Color", True)

        objConfig.Save()