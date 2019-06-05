import subprocess

def isWindowsProcessRunning(exeName) :
    import subprocess
    process = subprocess.Popen(
        'tasklist.exe /FO CSV /FI "IMAGENAME eq %s"' % exeName,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True )
    out, err = process.communicate()
    try :
        out.split("\n")[1].startswith('"%s"' % exeName)
        return True
    except : return False

rhinoPath = 'C:\Program Files\Rhino 6\System\Rhino.exe'
fileName = 'file.3dm'
scriptName = 'rhino3dScript.py'
scriptCall = ('-_RunPythonScript %s' % scriptName)
callCreateScript = ('"%s" /nosplash /notemplate /runscript="%s _-save %s _-exit"' % (rhinoPath, scriptCall, fileName))
callLoadScript = ('"%s" /nosplash /notemplate /runscript="_-open %s"' % (rhinoPath, fileName))
if (isWindowsProcessRunning('Rhino.exe')):
    subprocess.call('taskkill /f /im "Rhino.exe"')
subprocess.call(callCreateScript)
# subprocess.call(callLoadScript)

"""
RhinoScript commands:
_-RunPythonScript C:/Users/rhino3dScript.py
_-Circle x,y,z radius
_-Line x1,y1,z1 x2,y2,z2
_-Sphere x,y,z radius
_-save filename.3dm
_-open filename.3dm
_-exit
"""
