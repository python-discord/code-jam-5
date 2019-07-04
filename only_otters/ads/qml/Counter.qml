import QtQuick 2.7


Item {

    id: god
    property real value:        fact_counter.value
    property real offset:       fact_counter.offset
    property real interval:     fact_counter.interval
    property real precision:    fact_counter.precision
    // property real title:        fact_counter.title
    // property real subtitle:     fact_counter.subtitle

    function format(num) {
        num = '' + num.toFixed(precision);
        if (!precision) {
            num = num.replace(/(^\d{1,3}?)((?:\d{3})+)$/, '$1,$2') // put first comma
            if (num.includes(',')) {
                var [head, tail] = num.split(",") // process tail
                tail = tail.replace(/(\d{3})/, '$1,') // add , every 3 digits
                tail = tail.replace(/,$/, '') // remove trailing comma
                num = head + ',' + tail
            }
        }
        return num
    }

    Row {

        Text {
            text: format(god.value)// + ' [%1]'.arg(fact_counter.x)
            horizontalAlignment: Text.AlignRight
            width: 200

            Rectangle {
                anchors.fill: parent
                border.color: "#00B000"
                border.width: 1
                color: "transparent"
            }
        }

        Text {
            text: god.title
        }

    }

    Timer {
        id: timer
        repeat: true
        running: true
        interval: parent.interval
        onTriggered: parent.value += offset
    }

}
