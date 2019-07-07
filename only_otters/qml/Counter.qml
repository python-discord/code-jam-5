import QtQuick 2.7
import QtQuick.Layouts 1.0
import QtQuick.Controls 2.5
import QtQuick.Controls.Styles 1.4


Item {

    id: core
    property real value:        fact_counter.value
    property real offset:       fact_counter.offset
    property real interval:     fact_counter.interval
    property real precision:    fact_counter.precision
    property string fctext:     fact_counter.content

    anchors.fill: parent

    /**
    Produces a number format for rounded numbers (precision = 0)
    3000000 => 3,000,000
    */
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

    Rectangle {
        id: background
        anchors.fill: parent
        color: "#422d1e"
    }

    Column {

        spacing: 5
        padding: 8

        Text {
            id: number
            text: format(core.value)

            horizontalAlignment: Text.AlignRight
            font.pixelSize: 20
            font.bold: true
            color: "#fff"

        }

        Text {
            id: title
            text: core.fctext
            
            width: core.width * .9
            font.pixelSize: 15
            wrapMode: Text.WordWrap
            color: "#fff"
        }

    }

    Timer {
        id: timer
        repeat: true
        running: true
        interval: parent.interval
        onTriggered: parent.value += offset
    }

    Text {
        id: wsource
        
        text: '<html><a href="%1" style="color: #ad8365"> %1 </a></html>'.arg(fact_counter.source)

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
