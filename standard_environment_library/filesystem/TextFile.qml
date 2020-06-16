import QtQuick 2.7
import QtQuick.Controls 2.7

Item
{
    function updateData(data)
    {
        texture.width = data.icon_width;
        texture.height = data.icon_height;
        texture.anchors.leftMargin = texture.width / 2;

        texture.source = data.img_path;

        filename.color = data.color;
        filename.text = data.name;

        if(data.visible !== undefined)
            tag.visible = data.visible;
    }

    id: container

    visible: true

    Image {
        id: texture
        anchors.left: parent.left
        anchors.top: parent.top

        visible: true
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

    Rectangle {
       id: tag
       width: 15
       height: 15
       color: "blue"
       visible: false
    }
}