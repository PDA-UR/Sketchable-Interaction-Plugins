import QtQuick 2.7

Item {
    function updateData(data) {
        texture.width = data.widget_width;
        texture.height = data.widget_height;
        texture.source = data.img_path;
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
}






