import QtQuick

Item {
    id: container
    visible: true

    function updateData(data) {
        container.width = data.width;
        container.height = data.height;
        mouse_icon.width = data.height;
        mouse_icon.height = data.height;
        mouse_icon.source = data.img;
        text.width = container.width - mouse_icon.width;
        text.text = data.text;
    }

    Text {
        id: text
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
        text: "HELLO WORLD"
        wrapMode: Text.WordWrap
    }
    Image {
        id: mouse_icon
        anchors.right: parent.right
        visible: true
    }
}