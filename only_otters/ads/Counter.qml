
import QtQuick 2.7


Item {

    property alias text: label.text
    property alias color: background.color

    property real start: 33
    property real offset: -0.44
    property real interval: 200

    text: start.toFixed(0)

    Rectangle {
        id: background
        anchors.fill: parent
    }

    Text {
        id: label
    }

    Timer {
        id: timer
        repeat: true
        running: true
        interval: parent.interval
        onTriggered: parent.start += offset
    }

}