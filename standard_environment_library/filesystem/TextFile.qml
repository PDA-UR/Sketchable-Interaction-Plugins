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
        minimumPixelSize: 12
        font.pixelSize: 18
        color: "black"
        anchors.verticalCenter: texture.verticalCenter

        width: texture.width * 2
        anchors.top: texture.bottom
        anchors.left: texture.left

        wrapMode: Text.Wrap
    }

    Rectangle {
       id: tag
       width: 15
       height: 15
       color: "blue"
       visible: false
    }
}