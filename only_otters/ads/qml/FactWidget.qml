import QtQuick 2.7


Item {

    id: god
    property string title:    fact.title
    property string content:  fact.content
    property string source:   fact.source

    anchors.fill: parent

    Column {
        
        spacing: 0
        padding: 8

        Text {
            id: wtitle
            text: god.title

            font.pixelSize: 16
            font.bold: true

            wrapMode: Text.WordWrap
            width: god.width
        }

        Text {
            id: wcontent
            text: god.content
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignJustify
            width: god.width * 0.9
        }

    }

    Text {
        id: wsource
        // https://stackoverflow.com/questions/12536416/qml-text-element-hyperlink
        text: "<html><a href='%1'/> %1 </a></html>".arg(god.source)// fact_counter.source
        font.pixelSize: 12
        color: "#888"
        anchors.top: parent.top
        anchors.right: parent.right
        padding: 2
        onLinkActivated: Qt.openUrlExternally(link)
    }

}