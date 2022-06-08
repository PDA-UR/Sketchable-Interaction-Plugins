import QtQuick 2.7

Item
{
    function updateData(data) {
        texture.width = data.img_width;
        texture.height = data.img_height;
        texture.source = data.variable_image;

        texture.anchors.leftMargin = data.widget_width / 2 - texture.width / 2;
        texture.anchors.topMargin = data.widget_height / 2 - texture.height / 2;
    }

    id: container
    visible: true

    Image {
        id: texture
        anchors.left: parent.left
        anchors.top: parent.top
        asynchronous: true

        visible: true
    }

    Text {
        id: identifier
        visible: true

        fontSizeMode: Text.Fit
        minimumPixelSize: 16
        color: "black"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter

        wrapMode: TextEdit.Wrap
    }
}