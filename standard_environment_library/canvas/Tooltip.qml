import QtQuick 2.7

Item
{
    function updateData(data)
    {
        container.width = data.width;
        container.height = data.height;

        mouse_icon.width = data.height;
        mouse_icon.height = data.height;
        mouse_icon.source = data.img;

        text.width = container.width - mouse_icon.width;
        text.text = data.text;
    }

    id: container
    visible: true

    Text {
        id: text
        text: "HELLO WORLD"
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
        wrapMode: Text.WordWrap
    }

    Image {
        id: mouse_icon
        anchors.right: parent.right

        visible: true
    }
}