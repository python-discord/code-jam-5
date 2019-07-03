import QtQuick 2.7


Item {

    property real value:        3300
    property real offset:       -0.44
    property real interval:     1000
    property real precision:    0

    function format(num) {
        num = '' + num.toFixed(precision);
        if (!precision) {
            num = [...num].reverse().join(''); // Reverse string
            num = num.replace(/([0-9]{3})/, '$1,'); // Write commas
            num = [...num].reverse().join(''); // Reverse string
        }
        return num
    }

    Text {
        text: format(parent.value)
    }

    Timer {
        id: timer
        repeat: true
        running: true
        interval: parent.interval
        onTriggered: parent.value += offset
    }

}
