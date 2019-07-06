import QtQuick 2.7


Item {

    id: god
    property string title:    fact.title
    property string content:  fact.content
    property string source:   fact.source

    anchors.fill: parent

    Column {

        Text {
            id: wtitle
            text: god.title
            wrapMode: Text.WordWrap
            width: god.width
        }

        Text {
            id: wcontent
            text: god.content
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignJustify
            width: god.width
        }

    }

    Text {
        id: wsource
        text: "Source: %1".arg(god.source)
        anchors.bottom: parent.bottom
        anchors.right: parent.right
    }

}