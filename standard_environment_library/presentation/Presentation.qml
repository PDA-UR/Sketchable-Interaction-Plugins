import QtQuick 2.7

Item
{
    function updateData(data) {
        container.width = data.container_width
        container.height = data.container_height
        texture.width = data.img_width;
        texture.height = data.img_height;
        texture.source = data.img_path;

        if(!data.is_slide)
        {
            texture.anchors.leftMargin = data.widget_width / 2 - texture.width / 2;
            texture.anchors.topMargin = data.widget_height / 2 - texture.height / 2;
        }
        else
        {
            texture.anchors.leftMargin = 0;
            texture.anchors.topMargin = 0;
            texture.anchors.left = container.left;
            texture.anchors.top = container.top;
            opendirectorypagecount.visible = true;
            opendirectorypagecount.text = data.page;
            background.visible = true;
        }
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

    Rectangle {
            id: background
            color: "white"
            width: opendirectorypagecount.width + 10
            height: opendirectorypagecount.height + 10
            visible: false
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.topMargin: 50
            anchors.leftMargin: container.width * 0.5 - width * 0.5
        }

    Text {
        id: opendirectorypagecount
        visible: false
        fontSizeMode: Text.Fit
        minimumPixelSize: 16
        font.pixelSize: 48
        color: "black"
        width: 75
        anchors.bottom: parent.bottom
        anchors.left: parent.left

        anchors.topMargin: 50
        anchors.leftMargin: container.width * 0.5 - width * 0.5

        wrapMode: TextEdit.Wrap
        text: "0/0"
    }


}