import QtQuick

Item {
    id: container

    function updateData(data) {
        texture.width = data.img_width;
        texture.height = data.img_height;
        texture.source = data.img_path;
        container.width = data.width;
        container.height = data.height;
        texture.anchors.leftMargin = data.widget_width / 2 - texture.width / 2;
        texture.anchors.topMargin = data.widget_height / 2 - texture.height / 2;
    }

    visible: true

    Image {
        id: texture

        anchors.centerIn: parent
        asynchronous: true
        visible: true
    }
}