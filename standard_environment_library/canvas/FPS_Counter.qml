import QtQuick

Item {
    id: container
    visible: true

    function updateData(data) {
        te.text = data["text"];
    }

    Item {
        id: iconcontainer
        visible: true

        Text {
            id: te
            color: "black"
            font.family: "Helvetica"
            font.pointSize: 12
            horizontalAlignment: TextEdit.AlignHCenter
            text: "Hello World"
            verticalAlignment: TextEdit.AlignVCenter
            width: 100

            onTextChanged: REGION.set_data({
                    "text": te.text
                })
        }
    }
}