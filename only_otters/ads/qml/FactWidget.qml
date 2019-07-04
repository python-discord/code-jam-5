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
        }

        Text {
            id: wcontent
            text: god.content
        }

    }

    Text {
        id: wsource
        text: "Source: %1".arg(god.source)
        anchors.bottom: parent.bottom
        anchors.right: parent.right
    }

}