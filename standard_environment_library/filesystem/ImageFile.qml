import QtQuick 2.7
import QtQuick.Controls 2.7

Item
{
    function updateData(data)
    {
        container.visible = data.is_visible;

        texture.width = data.icon_width;
        texture.height = data.icon_height;

        if(data.is_in_preview)
            texture.anchors.leftMargin = 0;
        else
            texture.anchors.leftMargin = texture.width / 2;

        texture.source = "";
        texture.source = data.img_path;

        container.width = data.container_width
        container.height = data.container_height

        filename.color = data.color;
        filename.text = data.name;
        filename.visible = !data.is_in_preview;
    }

    id: container

    visible: true

    Image {
        id: texture
        anchors.left: parent.left
        anchors.top: parent.top
        fillMode: Image.PreserveAspectFit

        visible: true
        cache: false
    }

    Text {
        id: filename
        visible: true

        fontSizeMode: Text.Fit
        minimumPixelSize: 16
        font.pixelSize: 72
        color: "white"

        width: texture.width * 2
        anchors.top: texture.bottom
        anchors.left: texture.left
        anchors.topMargin: -10
        anchors.leftMargin: -width * 0.25

        wrapMode: TextEdit.Wrap
    }
}