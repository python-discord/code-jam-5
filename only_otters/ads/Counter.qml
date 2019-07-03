import QtQuick 2.7


Item {

    property real value:        fact_counter.value
    property real offset:       fact_counter.offset
    property real interval:     fact_counter.interval
    property real precision:    fact_counter.precision

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
