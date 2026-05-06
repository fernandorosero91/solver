Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Obtener el directorio del script
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Cambiar al directorio del script
WshShell.CurrentDirectory = scriptDir

' Verificar si existe el entorno virtual
pythonPath = scriptDir & "\venv\Scripts\pythonw.exe"
scriptPath = scriptDir & "\quiz_solver.py"

If Not fso.FileExists(pythonPath) Then
    MsgBox "Error: No se encontró el entorno virtual." & vbCrLf & vbCrLf & _
           "Por favor ejecuta primero:" & vbCrLf & _
           "  python -m venv venv" & vbCrLf & _
           "  venv\Scripts\activate" & vbCrLf & _
           "  pip install -r requirements.txt", _
           vbCritical, "QuizSnap - Error"
    WScript.Quit 1
End If

If Not fso.FileExists(scriptPath) Then
    MsgBox "Error: No se encontró quiz_solver.py", vbCritical, "QuizSnap - Error"
    WScript.Quit 1
End If

' Ejecutar sin ventana (0 = oculto, False = no esperar)
WshShell.Run """" & pythonPath & """ """ & scriptPath & """", 0, False

' Mostrar notificación de éxito
MsgBox "QuizSnap iniciado en segundo plano" & vbCrLf & vbCrLf & _
       "Hotkeys:" & vbCrLf & _
       "  Ctrl+Shift+Q = Captura completa" & vbCrLf & _
       "  Ctrl+Shift+S = Selección de región" & vbCrLf & _
       "  Ctrl+Shift+X = Salir", _
       vbInformation, "QuizSnap"
