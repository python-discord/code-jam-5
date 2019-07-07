import QtQuick 2.7


Item {

    id: core
    property string title:    fact.title
    property string content:  fact.content
    property string source:   fact.source

    anchors.fill: parent

    Rectangle {
        id: background

        anchors.fill: parent
        color: "#422d1e"
    }

    Column {
        
        spacing: 5
        padding: 8

        Text {
            id: wtitle
            text: core.title

            width: core.width * .9
            font.pixelSize: 16
            font.bold: true
            wrapMode: Text.WordWrap
            color: "#fff"
        }

        Text {
            id: wcontent
            text: core.content

            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignJustify
            width: core.width * .9
            color: "#fff"
        }

    }

    Text {
        id: wsource
        
        text: '<html><a href="%1" style="color: #ad8365"> %1 </a></html>'.arg(fact.source)

        anchors.bottom: parent.bottom
        anchors.right: parent.right

        wrapMode: Text.WrapAnywhere
        textFormat: Text.RichText
        horizontalAlignment: Text.AlignRight
        width: core.width
        font.underline: true
        font.pixelSize: 10
        padding: 5

        onLinkActivated: Qt.openUrlExternally(link)
    }

}