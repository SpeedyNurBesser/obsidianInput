import PySimpleGUI as sg
import yaml
import os

configFile = "config.yaml"


def loadConfig(configFile):
    with open(configFile) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config


def checkFileExistence(path):
    return os.path.isfile(path)


def popup_get_file(message, title=None, initialFolder=None):
    layoutGetFile = [
        [sg.Text(message)],
        [sg.Input(key='-INPUT-'), sg.FilesBrowse('Browse', initial_folder=initialFolder)],
        [sg.Button('Ok'), sg.Button('Cancel')],
    ]
    windowGetFile = sg.Window(title if title else message, layoutGetFile)
    eventGetFile, valuesGetFile = windowGetFile.read(close=True)
    return valuesGetFile['-INPUT-'] if eventGetFile == 'Ok' else None


def writeFile(file, mode, text, prependText=None):
    with open(file, mode) as f:
        if prependText != None:
            text = prependText + text

        f.write(text)
        f.close()

    automatic()


def prependWriteFile(file, text, prependText=None):
    if prependText != None:
        text = prependText + text

    if checkFileExistence(file):
        with open(file, "r") as f:
            original = f.read()
            f.close()
            text = text + "\n" + original

    with open(file, "w") as f:
        f.write(text)
        f.close()

    automatic()


TEXT_FONT = (loadConfig(configFile)['textFont'], int(loadConfig(configFile)['textFont-size']))
FONT = (loadConfig(configFile)['font'], int(loadConfig(configFile)['font-size']))
THEME = loadConfig(configFile)['theme']
VAULT_DIRECTORY = loadConfig(configFile)['vaultFolder']
IDEAS_DESTINATION = loadConfig(configFile)['ideasDestination']
IDEAS_PREPEND_TEXT = loadConfig(configFile)['ideasPrependAppendText']
IDEAS_PREPEND_PREPEND_TEXT = loadConfig(configFile)['ideasPrependPrependText']
AUTO_CLOSE = loadConfig(configFile)['autoClose']
AUTO_CLEAR = loadConfig(configFile)['autoClear']
AUTO_CLEAR_FILE = loadConfig(configFile)['autoClearFile']


sg.theme(THEME)


layout = [
         [sg.Multiline("", size=(80,20), font= TEXT_FONT, key= '--MultiLine--')],
         [sg.Button("New file", font= FONT, key= "--newFile--"), sg.Input(font= FONT, key= "--fileName--"), sg.Text(".md", font= FONT)],
         [sg.Button("Append to Ideas", font= FONT, key= "--ideasAppend--"), sg.Button("Prepend to Ideas", font= FONT, key= "--ideasPrepend--")],
         [sg.Button("Append to file", font= FONT, key= "--regularAppend--"), sg.Button("Prepend to file", font= FONT, key= "--regularPrepend--")]
    ]


window = sg.Window("Obsidian Input", layout)

def automatic():
    if not AUTO_CLOSE:
        if AUTO_CLEAR:
            window['--MultiLine--'].update("")
        if AUTO_CLEAR_FILE:
            window['--fileName--'].update("")
    else:
        quit()


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if values['--MultiLine--'] != "":
        if event == '--ideasAppend--':
            print("ideasAppend")
            if checkFileExistence(IDEAS_DESTINATION):
                writeFile(IDEAS_DESTINATION, "a", values['--MultiLine--'], IDEAS_PREPEND_TEXT)
            else:
                if sg.popup_yes_no(f"The file doesn't seem to exist. Do you want to create an ideas file at {IDEAS_DESTINATION}?") == "Yes":
                    print("0")
                    writeFile(IDEAS_DESTINATION, "a", values['--MultiLine--'], IDEAS_PREPEND_TEXT)
                else:
                    print("1")

        if event == '--regularAppend--':
            print("regularAppend")
            appendageLocation = popup_get_file("Select a file to append your text to.", "Select file", VAULT_DIRECTORY)
            if appendageLocation == None:
                pass
            elif appendageLocation == "":
                sg.popup_quick_message("No file specified.")
            else:
                if checkFileExistence(appendageLocation):
                    writeFile(appendageLocation, "a", values['--MultiLine--'])
                else:
                    sg.popup_quick_message("Specified file path doesn't exist.")

        if event == '--newFile--':
            print("newFile")
            if values['--fileName--'] != "":
                filename = f'{VAULT_DIRECTORY}\{values["--fileName--"]}.md'
                if checkFileExistence(filename):
                    overwrite = sg.popup_yes_no("Seems like a file with your specified filename already exists. Do you want to overwrite it? (all data inside will be deletetd)")
                    if overwrite == 'Yes':
                        writeFile(filename, "w", values['--MultiLine--'])
                    else:
                        pass
                    overwrite = None
                else:
                    writeFile(filename, "w", values['--MultiLine--'])
            else:
                sg.PopupQuickMessage("No file name specified.")




            #file exist? -> yes -> rewrite; no -> cancel

        if event == '--ideasPrepend--':
            print("ideasPrepend")
            if checkFileExistence(IDEAS_DESTINATION):
                prependWriteFile(IDEAS_DESTINATION,  values['--MultiLine--'], IDEAS_PREPEND_PREPEND_TEXT)
            else:
                if sg.popup_yes_no(f"The file doesn't seem to exist. Do you want to create an ideas file at {IDEAS_DESTINATION}?") == "Yes":
                    print("0")
                    prependWriteFile(IDEAS_DESTINATION, values['--MultiLine--'], IDEAS_PREPEND_PREPEND_TEXT)
                else:
                    print("1")

        if event == '--regularPrepend--':
            print("regularPrepend")
            appendageLocation = popup_get_file("Select a file to prepend your text to.", "Select file", VAULT_DIRECTORY)
            if appendageLocation == None:
                pass
            elif appendageLocation == "":
                sg.popup_quick_message("No file specified.")
            else:
                if checkFileExistence(appendageLocation):
                    prependWriteFile(appendageLocation, values['--MultiLine--'])
                else:
                    sg.popup_quick_message("Specified file path doesn't exist.")

    else:
        sg.PopupQuickMessage("No Input Text specified")


window.close()