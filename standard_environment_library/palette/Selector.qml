import QtQuick 2.7

Item
{
    function updateData(data)
    {
        texture.width = data.img_width;
        texture.height = data.img_height;
        texture.source = data.img_path;
        texture.anchors.leftMargin = data.width / 2 - texture.width / 2;
        texture.anchors.topMargin = data.height / 2 - texture.height * 1.25;

        if(data.visible)
            createAnimation.start();

        hover_text.visible = data.visible;

        hover_text.text = data.text;

        container.width = data.width;
        container.height = data.height;

        hover_text.width = data.width;
        hover_text.height = data.height;
    }

    id: container
    visible: true

    Text {
        NumberAnimation on opacity {
            id: createAnimation
            from: 0
            to: 1
            duration: 350
        }

        id: hover_text
        visible: false

        fontSizeMode: Text.Wrap
        font.pixelSize: 18
        color: "black"
        horizontalAlignment: Text.AlignHCenter
        anchors.top: parent.top

        anchors.topMargin: hover_text.height / 2 + hover_text.height / 12

        wrapMode: Text.Wrap
    }

    Image {
        id: texture
        anchors.left: parent.left
        anchors.top: parent.top

        visible: true
    }
}