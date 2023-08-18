import QtQuick
import QtQuick.Controls

Item {
    id: container
    function updateData(data) {
        texture.width = data.widget_height;
        texture.height = data.widget_height;
        texture.source = data.img_path;
        container.width = data.widget_width;
        container.height = data.widget_height;
    }

    Image {
        id: texture
        anchors.left: parent.left
        anchors.top: parent.top
        asynchronous: true
        visible: true
    }
    Rectangle {
        id: bg
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 5
        anchors.left: texture.right
        anchors.leftMargin: 5
        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.top: parent.top
        anchors.topMargin: 5
        border.color: "black"
        border.width: 1
        color: "white"
        height: parent.height
        visible: true
        width: parent.width
    }
    TextField {
        id: te
        anchors.bottom: parent.bottom
        anchors.left: texture.right
        anchors.right: parent.right
        anchors.top: parent.top
        color: "grey"
        focus: true
        font.family: "Helvetica"
        font.pointSize: 20
        text: "search"

        Keys.onPressed: {
        }
        Keys.onReturnPressed: {
            textChanged();
        }
        onTextChanged: REGION.set_data({
                "text": te.text
            })

        MouseArea {
            anchors.fill: parent

            onClicked: {
                te.text = "";
                te.color = "black";
            }
        }
    }
}
