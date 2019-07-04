import QtQuick 2.7
import QtQuick.Layouts 1.0
import QtQuick.Controls 2.5
import QtQuick.Controls.Styles 1.4


Item {

    id: god
    property real value:        fact_counter.value
    property real offset:       fact_counter.offset
    property real interval:     fact_counter.interval
    property real precision:    fact_counter.precision
    property string fctext:     fact_counter.text

    anchors.fill: parent

    function format(num) {
        num = '' + num.toFixed(precision);
        if (!precision) {
            num = num.replace(/(^\d{1,3}?)((?:\d{3})+)$/, '$1,$2') // put first comma
            if (num.includes(',')) {
                var [head, tail] = num.split(",") // process tail
                tail = tail.replace(/(\d{3})/g, '$1,') // add , every 3 digits
                tail = tail.replace(/,$/, '') // remove trailing comma
                num = head + ',' + tail
            }
        }
        return num
    }

    Column {

        spacing: 5
        padding: 8

        Text {
            id: number
            text: format(god.value)
            horizontalAlignment: Text.AlignRight

            font.pixelSize: 20
            font.bold: true

        }

        Text {
            id: title
            text: god.fctext
            font.pixelSize: 15
            width: god.width
            wrapMode: Text.WordWrap

        }

    }

    Timer {
        id: timer
        repeat: true
        running: true
        interval: parent.interval
        onTriggered: parent.value += offset
    }

    Button {
        text: "Next Fact"
        font.pixelSize: 14
        height: 20
        padding: 0
        highlighted: true
        anchors.right: parent.right
        anchors.top: parent.top
    }

    Text {
        id: wsource
        // https://stackoverflow.com/questions/12536416/qml-text-element-hyperlink
        text: "<html><a href='%1'/> here </a></html>".arg('http://theme.typora.io')// fact_counter.source
        font.pixelSize: 12
        color: "#888"
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        padding: 2
        onLinkActivated: Qt.openUrlExternally(link)
    }

}
